def line_parse(data):
    data = data.split()
    new_applicant = {'NAME_SURNAME': ' '.join([data[0], data[1]]),
    'physics': float(data[2]),
    'chemistry': float(data[3]),
    'math': float(data[4]),
    'computer science': float(data[5]),
    'special': float(data[6]),
    'priorities': [data[7], data[8], data[9]]}
    return new_applicant

def mean_scores(student, related_exams):
    mean_score = 0
    for exam in related_exams:
        mean_score += student[exam]
    mean_score /= len(related_exams)
    return round(mean_score, 1)


applicants_list = []
applicant_file = open('applicant_list_7.txt', 'r')
for line in applicant_file:
    applicants_list.append(line_parse(line))
applicant_file.close()

dept_capacity = int(input())
dept_names = {'Biotech': ['chemistry', 'physics'],
             'Chemistry': ['chemistry'],
             'Engineering': ['computer science', 'math'],
             'Mathematics': ['math'],
             'Physics': ['physics', 'math']}
students = {dep_name: [] for dep_name in dept_names.keys()}

for priority in range(len(applicants_list[0]['priorities'])):
    if len(applicants_list) > 0:
        current_wave = {dep_name: [] for dep_name in dept_names.keys()}
        for applicant in applicants_list:
            desired_dep = applicant['priorities'][priority]
            current_wave[desired_dep].append(applicant)
        applicants_list = []
        for dep_name in students.keys():
            related_exams = dept_names[dep_name]
            current_wave[dep_name].sort(reverse=True,
                                         key=lambda x: (-max(mean_scores(x, related_exams), x['special']),
                                                        x['NAME_SURNAME']))
            if len(students[dep_name]) < dept_capacity:
                while (len(students[dep_name]) < dept_capacity)\
                        and (len(current_wave[dep_name]) > 0):
                    students[dep_name].append(current_wave[dep_name].pop())
            applicants_list.extend(current_wave[dep_name])
    else:
        break

for dep_name, dep_students in students.items():
    file = open(dep_name + '.txt', 'w', encoding='utf-8')
    related_exams = dept_names[dep_name]
    dep_students.sort(key=lambda x: (-max(mean_scores(x, related_exams), x['special']), x['NAME_SURNAME']))
    for student in dep_students:
        file.write(' '.join([student['NAME_SURNAME'],
                             str(max(mean_scores(student, related_exams),
                                     student['special']))]) + '\n')
    file.close()
