from django.db import models


class Genders(models.Model):
    code = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return self.gender


class Degrees(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Ranks(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    code = models.CharField(max_length=20, unique=True)
    faculty = models.CharField(max_length=200)

    def __str__(self):
        return self.faculty


class Department(models.Model):
    code = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=200)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, to_field='code')

    def __str__(self):
        return self.department


class EmploymentForm(models.Model):
    code = models.CharField(max_length=20, unique=True)
    employmentForm = models.CharField(max_length=50)

    def __str__(self):
        return self.employmentForm


class EmployeeType(models.Model):
    code = models.CharField(max_length=20, unique=True)
    employeeType = models.CharField(max_length=50)

    def __str__(self):
        return self.employeeType


class EmployeeStatus(models.Model):
    code = models.CharField(max_length=20, unique=True)
    employeeStatus = models.CharField(max_length=50)

    def __str__(self):
        return self.employeeStatus


class EmploymentStaff(models.Model):
    code = models.CharField(max_length=20, unique=True)
    employmentStaff = models.CharField(max_length=50)

    def __str__(self):
        return self.employmentStaff


class StaffPosition(models.Model):
    code = models.CharField(max_length=20, unique=True)
    staffPosition = models.CharField(max_length=50)

    def __str__(self):
        return self.staffPosition


class Teachers(models.Model):
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    third_name = models.CharField(max_length=50)
    employee_id_number = models.BigIntegerField()
    gender = models.ForeignKey(Genders, on_delete=models.CASCADE, to_field='code')
    birth_date = models.CharField(max_length=100)
    image = models.URLField()
    year_of_enter = models.CharField(max_length=20)
    academicDegree = models.ForeignKey(Degrees, on_delete=models.CASCADE, to_field='code')
    academicRank = models.ForeignKey(Ranks, on_delete=models.CASCADE, to_field='code')
    academic_degree_data = models.ForeignKey('AcademicDegreeData', on_delete=models.SET_NULL, related_name='academic_degree_data_name', null=True, blank=True)
    academic_rank_data = models.ForeignKey('AcademicRankData', on_delete=models.SET_NULL, related_name='academic_rank_data_name', null=True, blank=True)

    language_cert = models.ForeignKey('LanguageCert', on_delete=models.SET_NULL, related_name='language_cert_name', null=True, blank=True)

    department = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='code')
    employmentForm = models.ForeignKey(EmploymentForm, on_delete=models.CASCADE, to_field='code')
    employmentStaff = models.ForeignKey(EmploymentStaff, on_delete=models.CASCADE, to_field='code')
    staffPosition = models.ForeignKey(StaffPosition, on_delete=models.CASCADE, to_field='code')
    employeeStatus = models.ForeignKey(EmployeeStatus, on_delete=models.CASCADE, to_field='code')
    employeeType = models.ForeignKey(EmployeeType, on_delete=models.CASCADE, to_field='code')
    contact_number = models.CharField(max_length=100)
    decree_number = models.CharField(max_length=100, null=True, blank=True)
    contact_date = models.CharField(max_length=100, null=True, blank=True)
    decree_date = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.CharField(max_length=100, null=True, blank=True)
    updated_at = models.CharField(max_length=100, null=True, blank=True)
    hash = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class AcademicDegreeData(models.Model):
    place_of_defense_degree = models.CharField(max_length=200, null=True, blank=True)
    council_number_degree = models.CharField(max_length=200, null=True, blank=True)
    given_by_whom_degree = models.CharField(max_length=100, null=True, blank=True)
    date_of_defense_degree = models.DateField(null=True, blank=True)
    number_of_degree_degree = models.CharField(max_length=100, null=True, blank=True)
    confirmed_date_degree = models.DateField(null=True, blank=True)
    account_number_degree = models.CharField(max_length=100, null=True, blank=True)
    created_degree = models.DateField(null=True, blank=True)
    changed_degree = models.DateField(null=True, blank=True)
    academic_degree_file_degree = models.FileField(upload_to='academicDegree/', null=True, blank=True)

    def __str__(self):
        return str(self.place_of_defense_degree)


class AcademicRankData(models.Model):
    place_of_defense_rank = models.CharField(max_length=200, null=True, blank=True)
    council_number_rank = models.CharField(max_length=200, null=True, blank=True)
    given_by_whom_rank = models.CharField(max_length=100, null=True, blank=True)
    date_of_defense_rank = models.DateField(null=True, blank=True)
    number_of_degree_rank = models.CharField(max_length=100, null=True, blank=True)
    confirmed_date_rank = models.DateField(null=True, blank=True)
    account_number_rank = models.CharField(max_length=100, null=True, blank=True)
    created_rank = models.DateField(null=True, blank=True)
    changed_rank = models.DateField(null=True, blank=True)
    academic_rank_file_rank = models.FileField(upload_to='academicRank/', null=True, blank=True)

    def __str__(self):
        return str(self.place_of_defense_rank)


class LanguageCert(models.Model):
    cert_type = models.CharField(max_length=200, null=True, blank=True)
    cert_file = models.FileField(upload_to='langCert/', null=True, blank=True)

    def __str__(self):
        return str(self.cert_type)


class Grants(models.Model):
    grand_1 = models.PositiveIntegerField(default=0)
    grand_2 = models.PositiveIntegerField(default=0)
    summa = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.grand_1)