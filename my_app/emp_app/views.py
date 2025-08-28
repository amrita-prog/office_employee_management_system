from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Employee, Role, Department, Attendance
from datetime import datetime
from django.utils import timezone
from django.db.models import Q, Count

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def dashboard(request):
    today = timezone.now().date()
    stats = {
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
        'hires_this_month': Employee.objects.filter(hire_date__year=today.year, hire_date__month=today.month).count(),
        'present_today': Attendance.objects.filter(date=today, status='Present').count(),
    }
    recent_employees = Employee.objects.order_by('-hire_date')[:5]

    hires_by_month = (
        Employee.objects
        .values('hire_date__year', 'hire_date__month')
        .annotate(total=Count('id'))
        .order_by('hire_date__year', 'hire_date__month')
    )

    return render(request, 'dashboard.html', {
        'stats': stats,
        'recent_employees': recent_employees,
        'hires_by_month': hires_by_month,
    })

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    print(context)
    return render(request, 'view_all_emp.html',context)

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
        messages.success(request, 'Employee added successfully')
        return render(request, 'employee_success.html', {'message': 'Employee added successfully'})
    
        
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    
    else :
        return HttpResponse('An Exception Occured! Employee Has Not Been Added')

def employee_detail(request, emp_id: int):
    try:
        employee = Employee.objects.get(id=emp_id)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found')
        return redirect('all_emp')
    return render(request, 'employee_detail.html', {'employee': employee})

def employee_edit(request, emp_id: int):
    try:
        employee = Employee.objects.get(id=emp_id)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found')
        return redirect('all_emp')

    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name', employee.first_name)
        employee.last_name = request.POST.get('last_name', employee.last_name)
        employee.salary = int(request.POST.get('salary', employee.salary))
        employee.bonus = int(request.POST.get('bonus', employee.bonus))
        employee.phone = int(request.POST.get('phone', employee.phone))
        employee.dept_id = int(request.POST.get('dept', employee.dept_id))
        employee.role_id = int(request.POST.get('role', employee.role_id))
        employee.save()
        messages.success(request, 'Employee updated successfully')
        return redirect('all_emp')

    return render(request, 'employee_edit.html', {'employee': employee})


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
    
    query = request.GET.get('q', '').strip()
    emps = Employee.objects.all()
    if query:
        if query.isdigit():
            emps = emps.filter(Q(id=int(query)) | Q(phone__icontains=query))
        else:
            emps = emps.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    return render(request, 'remove_emp.html', {'emps': emps, 'q': query})


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
