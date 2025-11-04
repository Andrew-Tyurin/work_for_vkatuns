from django.contrib.auth.models import User
from django.core.files import File

from main.models import Company, Specialty, Vacancy, Application, Resume
from data import users, companies, specialties, jobs, applications, resume_all


allow_recording = False

'''
Зайти как админ: (admin, admin1234)
Остальные пользователи(user_1 - user_9, user1234)
'''


def write_data():
    admin = User(
        username='admin',
        email='admi@mail.ru',
        is_superuser=True,
        is_staff=True,
        is_active=True,
    )
    admin.set_password('admin1234')
    admin.save()
    print(admin)

    for item in users:
        user = User(
            username=item['username'],
            first_name=item['first_name'],
            last_name=item['last_name'],
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )
        user.set_password('user1234')
        user.save()
        print(user)

    for item in companies:
        with open('./main/images/companies/' + item['logo'], 'rb') as f:
            company = Company(
                name=item['title'],
                location=item['location'],
                employee_count=item['employee_count'],
                description=item['description'],
                owner_id=item['owner_id'],
            )
            company.save()
            company.logo.save(item['logo'], File(f), save=True)
            print(company)

    for item in specialties:
        with open('./main/images/specialties/' +  item['picture'], 'rb') as f:
            specialty = Specialty(
                code=item['code'],
                title=item['title'],
            )
            company.save()
            specialty.picture.save(item['picture'], File(f), save=True)
            print(specialty)

    for item in jobs:
        vacancy = Vacancy.objects.create(
            title=item['title'],
            specialty_id=item['specialty'],
            company_id=item['company_id'],
            skills=item['skills'],
            description=item['description'],
            salary_min=item['salary_from'],
            salary_max=item['salary_to'],
        )
        print(vacancy)

    for item in applications:
        application = Application.objects.create(
            written_username=item['written_username'],
            written_cover_letter=item['written_cover_letter'],
            written_phone=item['written_phone'],
            vacancy_id=item['vacancy_id'],
            user_id=item['user_id'],
        )
        print(application)

    for item in resume_all:
        resume = Resume.objects.create(
            name=item['name'],
            surname=item['surname'],
            status=item['status'],
            salary=item['salary'],
            grade=item['grade'],
            education=item['education'],
            specialty_id=item['specialty_id'],
            user_id=item['user_id'],
        )
        print(resume)


if allow_recording:
    write_data()
