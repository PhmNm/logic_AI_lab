import os
    
# Các mệnh đề dạng hội chuẩn CNF được lưu bằng danh sách các literal bên trong ( Ví dụ: P v Q v -R => ['P','Q','-R'] )
# KB và alpha là danh sách chứa các mệnh đề ( Ví dụ: KB = -P ; P v Q => [['-P'],['P','Q']] )

#Các hàm hỗ trợ hợp giải
##1. Tìm phủ định của literal
def get_neg_lit(lit):
    if lit[0] == '-':
        return lit.strip('-')
    return '-' + lit

##2. Tìm phủ định của mệnh đề CNF (chuyển từ phép OR --> AND) ( Ví dụ: A OR -B --> -A AND B => ['A','-B'] --> [['-A'],['B']] )
def get_neg_clause(clause):
    new_clause = []
    for lit in clause:
        new_clause.append([get_neg_lit(lit)])
    return new_clause

##3. Sắp xếp các literal theo thứ tự chữ cái
def sorted_clause(clause):
    temp_clause = {}
    for i in clause:
        if i[0] == '-':
            temp_clause[i] = i[1]
        else: temp_clause[i] = i
    new_clause = sorted(temp_clause.keys(), key=lambda x: temp_clause[x])
    return new_clause

##4. Đọc file
def read_file(file_name):
    KB = []
    alpha = []
    with open(file_name,'r') as fin:
        lines = fin.readlines()
        alpha = lines[0].strip().split('OR')
        for i in range(len(alpha)):
            alpha[i] = alpha[i].strip(' ')
        for line in lines[2:]:
            line = line.strip().split('OR')
            for i in range(len(line)):
                line[i] = line[i].strip(' ')
            KB.append(sorted_clause(line))
    return KB,alpha

##5. Xuất file
def write_output(file_name,res,list_solutions):
    with open(file_name,'w') as fout:
        for round in list_solutions:
            fout.write(str(len(round)) + '\n')
            for clause in round:
                if len(clause) == 0:
                    fout.write('{}\n')
                for i in range(len(clause)):
                    fout.write(clause[i])
                    if i != len(clause) - 1: fout.write(' OR ')
                    else: fout.write('\n')
        if res == True: fout.write('YES')
        else: fout.write('NO')
        return 1
    return 0

##6. Kiểm tra xem 2 mệnh đề có hợp giải với nhau được không
def resolvable (clauseA,clauseB):
    count = 0
    for lit in clauseA:
        neg_lit = get_neg_lit(lit)
        if  neg_lit in clauseB: count += 1
    if count == 1: return True              #Nếu giữa 2 mệnh đề A B chỉ tồn tại đúng 1 cặp literal đối nhau thì 2 mệnh đề 'hợp giải được'
    else:
        return False

# Hợp giải 2 mệnh đề
def resolve(clauseA,clauseB):
    new_clause = []
    for lit in clauseA:                     
        neg_lit = get_neg_lit(lit)
        if  neg_lit in clauseB:                         #Thêm tất cả những literal không đối nhau vào mệnh đề mới
            for left in clauseA:
                if left != lit:
                    new_clause.append(left)
            for left in clauseB:
                if left != neg_lit:
                    new_clause.append(left)
            new_clause = sorted_clause(set(new_clause)) #sort lại những literal trong mệnh đề mới (literal trùng nhau chỉ lấy 1)
            return new_clause
    return None

# Giải thuật hợp giải
def PL_resolution(KB, alpha):
    clauses = KB
    clauses += get_neg_clause(alpha)
    news = []                           #Danh sách news chứa những danh sách mệnh đề mới (new) được tạo ra trong 1 vòng lặp
    while True:
        new = []
        for i in range(len(clauses)-1):
            for j in range(i,len(clauses)):
                if clauses[i] == clauses[j] or (not resolvable(clauses[i], clauses[j])): #Nếu 2 mệnh đề trùng nhau / không thể hợp giải
                    continue
                else:
                    new_clause = resolve(clauses[i], clauses[j])
                    if new_clause not in clauses and new_clause not in new:             #Nếu mệnh đề mới không trong KB và không được đã tạo ra trong cùng vòng lặp
                        new.append(new_clause)
                        print(str(new_clause) + ' == ' + str(clauses[i]) + ' -- ' + str(clauses[j]))
        news.append(new)
        if all([i in clauses for i in new]):
            return False, news
        elif [] in new:return True,news
        clauses += new                                                                  #Thêm những mệnh đề mới vào KB

### Main
path_in = '.\\input'
path_out = '.\\output'
output_name = 'output{i}.txt' #số thứ tự trong tên file output phụ thuộc vào số thứ tự của file input trong thư mục input
i = 1
if not os.path.exists(path_out): ##Không nhất thiết phải tạo trước folder 'output'
    os.mkdir(path_out)
for input_file_name in os.listdir(path_in):
    input = path_in + '\\' + input_file_name
    output = path_out + '\\' + output_name.format(i=i) 
    KB, alpha = read_file(input)
    res, list_solutions = PL_resolution(KB, alpha)
    output_res = write_output(output, res, list_solutions)
    if output_res == 0:
        print('Xuất file ' + output_name.format(i=i) + ' không thành công')
    else:     print('Xuất file ' + output_name.format(i=i) + ' thành công')
    i += 1