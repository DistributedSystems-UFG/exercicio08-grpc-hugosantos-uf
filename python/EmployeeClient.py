from __future__ import print_function
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

import const

def run():
    with grpc.insecure_channel(const.IP+':'+const.PORT) as channel:
        stub = EmployeeService_pb2_grpc.EmployeeServiceStub(channel)

        # Query an employee's data
        response = stub.GetEmployeeDataFromID(EmployeeService_pb2.EmployeeID(id=101))
        print ('Employee\'s data: ' + str(response))

        # Add a new employee
        response = stub.CreateEmployee(EmployeeService_pb2.EmployeeData(id=301, name='Jose da Silva', title='Programmer'))
        print ('Added new employee ' + response.status)

        # Change an employee's title
        response = stub.UpdateEmployeeTitle(EmployeeService_pb2.EmployeeTitleUpdate(id=301, title='Senior Programmer'))
        print ('Updated employee ' + response.status)

        # Delete an employee
        response = stub.DeleteEmployee(EmployeeService_pb2.EmployeeID(id=201))
        print ('Deleted employee ' + response.status)

        # List all employees
        response = stub.ListAllEmployees(EmployeeService_pb2.EmptyMessage())
        print ('All employees: ' + str(response))

        # Count employees
        response = stub.CountEmployees(EmployeeService_pb2.EmptyMessage())
        print ('Employee count: ' + str(response.count))

        # List employees by title
        response = stub.ListEmployeesByTitle(EmployeeService_pb2.EmployeeTitleQuery(title='Senior Programmer'))
        print ('Employees with title Senior Programmer: ' + str(response))

        # Update an employee's name
        response = stub.UpdateEmployeeName(EmployeeService_pb2.EmployeeNameUpdate(id=301, name='Jose Santos'))
        print ('Updated employee name ' + response.status)

        response = stub.GetEmployeeDataFromID(EmployeeService_pb2.EmployeeID(id=301))
        print ('Updated employee data: ' + str(response))

if __name__ == '__main__':
    logging.basicConfig()
    run()
