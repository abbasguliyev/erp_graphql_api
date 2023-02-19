from django.test import TestCase
from company.models import Holding, Company, Office, Department

class DepartmentTest(TestCase):
    def setUp(self) -> None:
        self.holding = Holding(name="Holding")
        self.holding.save()
        self.company = Company(name="Company", holding=self.holding)
        self.company.save()
        self.office = Office(name="Office", company=self.company)
        self.office.save()
        self.department = Department(name="Department", office=self.office)
        self.department.save()
        
    def tearDown(self) -> None:
        self.holding.delete()
        
    def test_read_department(self):
        self.assertEqual(self.department.name, "Department")
        self.assertEqual(self.department.office, self.office)
        self.assertEqual(self.department.is_active, True)
    
    def test_update_department_name(self):
        self.department.name = "Department2"
        self.department.save()
        self.assertEqual(self.department.name, "Department2")
        
    def test_update_department_is_active(self):
        self.department.is_active =False
        self.department.save()
        self.assertEqual(self.department.is_active, False)
        
    