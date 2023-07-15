# task1
print("===task1===")
def find_and_print(messages):
    # 提到"I'm 18 years old" 
    # 或是"I'm a college student"
    # 或是"I am of legal age"
    for x in messages:
        if "I'm 18 years old" in messages[x]:
            print(x)
        elif "I'm a college student" in messages[x]:
            print(x)
        elif "I am of legal age" in messages[x]:
            print(x)

find_and_print({
    "Bob":"My name is Bob. I'm 18 years old.", 
    "Mary":"Hello, glad to meet you.",
    "Copper":"I'm a college student. Nice to meet you.", 
    "Leslie":"I am of legal age in Taiwan.",
    "Vivian":"I will vote for Donald Trump next week", 
    "Jenny":"Good morning."
})


# task2
print("===task2===")
def calculate_sum_of_bonus(data):
    # 表現 "高於平均":薪水的10%, "平均":薪水的5%, "低於平均":0
    # 職位 "CEO":bonus*1.1, "工程師":bonus*1.05, "銷售":bonus*1.05
    all_bonus = 0
    for x in data['employees']:
        salary = 0
        if type(x['salary']) == str:
            if 'USD' in x['salary']:
                salary = int(x['salary'][:-3])*30
            elif ',' in x['salary']:
                salary = int(x['salary'].replace(',',''))
        else:
            salary = x['salary']
        bonus = 0
        if x['performance'] == 'above average':
            bonus = salary * 0.1
        elif x['performance'] == 'average':
            bonus = salary * 0.05
        if x['role'] == 'CEO':
            bonus *= 1.1
        elif x['role'] == 'Engineer' or 'Sales':
            bonus *= 1.05
        all_bonus += bonus
    print(all_bonus)
calculate_sum_of_bonus({ 
    "employees":[
        {
            "name":"John",
            "salary":"1000USD", 
            "performance":"above average", 
            "role":"Engineer"
        }, 
        {
            "name":"Bob", 
            "salary":60000, 
            "performance":"average", 
            "role":"CEO"
        }, 
        {
            "name":"Jenny", 
            "salary":"50,000", 
            "performance":"below average", 
            "role":"Sales"
        } 
    ]
}) # call calculate_sum_of_bonus function


# task3
print("===task3===")
def func(*data):
    unique_mid = []
    for x in data:
        if x[1] not in unique_mid:
            unique_mid.append(x[1])
        else:
            unique_mid.remove(x[1])
    if unique_mid:
        for x in data:
            for y in unique_mid:
                if x[1] == y:
                    print(x)
    else:
        print("沒有")
func("彭大牆", "王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花") # print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有


# task4
print("===task4===")
def get_number(index):
    if index == 0:
        ans = 0
    elif index%2 == 0:
        ans = index/2*3
    else:
        ans = index*1.5+2.5
    print(int(ans))
get_number(1) # print 4
get_number(5) # print 10 
get_number(10) # print 15

'''
# task5
def find_index_of_car(seats, status, number):
    # your code here
find_index_of_car([3, 1, 5, 4, 2], [0, 1, 0, 1, 1], 2) # print 4 
find_index_of_car([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # print -1 
find_index_of_car([4, 6, 5, 8], [0, 1, 1, 1], 4) # print 2
'''
