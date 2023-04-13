from typing import Dict
import time
import requests
from django.shortcuts import render

from .models import *

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer CkqR11YTBVhJDB_TPXPJ5Nj4eLuOvPA-'}

url = 'https://student.tersu.uz/rest/v1/data/employee-list'


def saveData():
    def get_employee_data(page):
        response = requests.get(url, params={'type': 'teacher', 'limit': 200, 'page': page}, headers=headers)
        response.raise_for_status()
        return response.json()['data']['items']

    def extract_unique_values(employee_data, key):
        values = set()
        for employee in employee_data:
            values.add(f"{employee[key]['code']} - {employee[key]['name']}")
        return values

    response = requests.get(url, params={'type': 'teacher', 'limit': 200, 'page': 1}, headers=headers)
    response.raise_for_status()

    total_page = response.json()['data']['pagination']['pageCount']
    employee_data = response.json()['data']['items']

    for page in range(2, total_page + 1):
        employee_data += get_employee_data(page)

    time.sleep(1)
    gender_values = extract_unique_values(employee_data, 'gender')
    for gender_value in gender_values:
        code, name = gender_value.split(" - ")
        Genders.objects.get_or_create(code=code, gender=name)

    time.sleep(1)
    academic_degree_values = extract_unique_values(employee_data, 'academicDegree')
    for academic_degree_value in academic_degree_values:
        code, name = academic_degree_value.split(" - ")
        Degrees.objects.get_or_create(code=code, name=name)

    time.sleep(1)
    academic_rank_values = extract_unique_values(employee_data, 'academicRank')
    for academic_rank_value in academic_rank_values:
        code, name = academic_rank_value.split(" - ")
        Ranks.objects.get_or_create(code=code, name=name)

    time.sleep(1)
    employment_form_values = extract_unique_values(employee_data, 'employmentForm')
    for employment_form_value in employment_form_values:
        code, name = employment_form_value.split(" - ")
        EmploymentForm.objects.get_or_create(code=code, employmentForm=name)

    time.sleep(1)
    employment_staff_values = extract_unique_values(employee_data, 'employmentStaff')
    for employment_staff_value in employment_staff_values:
        code, name = employment_staff_value.split(" - ")
        EmploymentStaff.objects.get_or_create(code=code, employmentStaff=name)

    time.sleep(1)
    staff_position_values = extract_unique_values(employee_data, 'staffPosition')
    for staff_position_value in staff_position_values:
        code, name = staff_position_value.split(" - ")
        StaffPosition.objects.get_or_create(code=code, staffPosition=name)

    time.sleep(1)
    employment_status_values = extract_unique_values(employee_data, 'employeeStatus')
    for employment_status_value in employment_status_values:
        code, name = employment_status_value.split(" - ")
        EmployeeStatus.objects.get_or_create(code=code, employeeStatus=name)

    time.sleep(1)
    employment_type_values = extract_unique_values(employee_data, 'employeeType')
    for employment_type_value in employment_type_values:
        code, name = employment_type_value.split(" - ")
        EmployeeType.objects.get_or_create(code=code, employeeType=name)



def saveFacultet():
    response = requests.get('https://student.tersu.uz/rest/v1/data/department-list?limit=200', headers=headers)
    data = response.json()

    for item in data['data']['items']:
        if item['structureType']['code'] == '11':
            Faculty.objects.get_or_create(code=item['id'], faculty=item['name'])


def saveDepartment():
    response = requests.get('https://student.tersu.uz/rest/v1/data/department-list?limit=200', headers=headers)
    data = response.json()

    for item in data['data']['items']:
        if item['structureType']['code'] == '12':
            faculty = Faculty.objects.get(code=item['parent'])
            Department.objects.get_or_create(code=item['code'], department=item['name'], faculty_id=faculty)


def saveTeacher():
    response = requests.get('https://student.tersu.uz/rest/v1/data/employee-list?type=teacher&&limit=200&&page=1',
                            headers=headers)
    pageCount = response.json()['data']['pagination']['pageCount']
    data = response.json()['data']['items']
    for page in range(2, pageCount + 1):
        response = requests.get(
            f'https://student.tersu.uz/rest/v1/data/employee-list?type=teacher&&limit=200&&page={page}',
            headers=headers)
        data_1 = response.json()['data']['items']
        data += data_1

    # print(len(data))
    #     print(data)
    # print(data[0]['id'])

    for i in data:
        teacher = Teachers()
        teacher.full_name = i['full_name']
        teacher.short_name = i['short_name']
        teacher.first_name = i['first_name']
        teacher.second_name = i['second_name']
        teacher.third_name = i['third_name']
        teacher.image = i['image']
        teacher.year_of_enter = i['year_of_enter']
        teacher.employee_id_number = i['employee_id_number']

        teacher.gender = Genders.objects.get(code=i['gender']['code'])
        teacher.department = Department.objects.get(code=i['department']['code'])
        teacher.academicDegree = Degrees.objects.get(code=i['academicDegree']['code'])
        teacher.academicRank = Ranks.objects.get(code=i['academicRank']['code'])
        teacher.employmentForm = EmploymentForm.objects.get(code=i['employmentForm']['code'])
        teacher.employmentStaff = EmploymentStaff.objects.get(code=i['employmentStaff']['code'])
        teacher.staffPosition = StaffPosition.objects.get(code=i['staffPosition']['code'])
        teacher.employeeStatus = EmployeeStatus.objects.get(code=i['employeeStatus']['code'])
        teacher.employeeType = EmployeeType.objects.get(code=i['employeeType']['code'])

        teacher.contract_number = i['contract_number']
        teacher.decree_number = i['decree_number']
        teacher.contract_date = i['contract_date']
        teacher.decree_date = i['decree_date']
        teacher.birth_date = i['birth_date']
        teacher.created_at = i['created_at']
        teacher.update_at = i['updated_at']
        teacher.hash = i['hash']
        teacher.save()


def Merge():
    all_employees = Teachers.objects.all()

    # Loop through each employee
    for employee in all_employees:
        # Get all positions for the current employee
        i = Teachers.objects.filter(employee_id_number=employee.employee_id_number)

        # Create a new employee instance with the common fields shared by all positions
        merged_employee = Teachers()

        for field in Teachers._meta.fields:
            try:
                setattr(merged_employee, field.name, getattr(i[0], field.name))
            except AttributeError:
                setattr(merged_employee, field.name, "")

        # Update the merged employee instance with fields from each position
        for position in i:
            merged_employee.employmentForm += position.employmentForm
            merged_employee.employmentStaff += position.employmentStaff

            # Add other fields specific to each position here...

        # Save the merged employee instance to the database
        merged_employee.save()

        # Delete the original employee positions from the database
        i.delete()