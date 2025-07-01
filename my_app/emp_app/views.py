from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Employee, Role, Department, Attendance
from datetime import datetime
from django.utils import timezone
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    print(context)
    return render(request, 'view_all_emp.html',context)

# Add Employee
def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        dept = int(request.POST['dept'])
        phone = int(request.POST['phone'])
        role = int(request.POST['role'])

        new_emp = Employee(first_name = first_name,last_name = last_name,salary = salary,bonus = bonus,dept_id = dept,phone = phone,role_id = role,hire_date = datetime.now())

        new_emp.save()

        return HttpResponse('Employee Added Successfully')
    
        
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    
    else :
        return HttpResponse('An Exception Occured! Employee Has Not Been Added')

# Remove Employee
def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp = Employee.objects.get(id=emp_id)
            emp.delete()
            messages.success(request, "✅ Employee Removed Successfully!")
            return redirect('remove_emp_list')
        except Employee.DoesNotExist:
            messages.error(request, "❌ Valid Employee ID nahi mila.")
            return redirect('remove_emp')
    
    emps = Employee.objects.all()
    return render(request, 'remove_emp.html', {'emps': emps})

# Filter Employee
def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps' : emps 
        }
        return render(request, 'view_all_emp.html',context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    
    else:
        return HttpResponse('An Exception Occured!')
    
# Mark Attendance
def mark_attendance(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        emp_id = request.POST.get('employee')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        status = request.POST.get('status')

        employee = Employee.objects.get(id=emp_id)
        Attendance.objects.create(
            employee=employee,
            date=timezone.now().date(),
            check_in=check_in,
            check_out=check_out,
            status=status
        )
        return render(request, 'mark_attendance.html', {'employees': employees, 'message': 'Attendance marked successfully!'})

    return render(request, 'mark_attendance.html', {'employees': employees})


def view_attendance(request):
    attendance_records = Attendance.objects.all().order_by('-date')
    return render(request, 'view_attendance.html', {'attendance': attendance_records})
