from user_company import models
from data import *

flag_Company, flag_Specialty, flag_Vacancy = False, False, False

if flag_Company:
    for item in companies:
        obj = models.Company.objects.create(
            name=item['title'],
            location=item['location'],
            employee_count=item['employee_count'],
            description=item['description']
        )
        print(obj)

if flag_Specialty:
    for item in specialties:
        obj = models.Specialty.objects.create(
            code=item['code'],
            title=item['title'],
        )
        print(obj)

if flag_Vacancy:
    for item in jobs:
        obj = models.Vacancy.objects.create(
            title=item['title'],
            specialty_id=item['specialty'],
            company_id=int(item['company']),
            skills=item['skills'],
            description=item['description'],
            salary_min=int(item['salary_from']),
            salary_max=int(item['salary_to']),
        )
        print(obj)

db_check = False
if db_check:
    for obj in models.Company.objects.all():
        print(obj)
    print()
    for obj in models.Vacancy.objects.all():
        print(obj)
    print()
    for obj in models.Specialty.objects.all():
        print(obj)
