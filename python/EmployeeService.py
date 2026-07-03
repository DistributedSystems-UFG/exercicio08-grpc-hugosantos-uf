from concurrent import futures
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc

import const

empDB=[
 {
 'id':101,
 'name':'Saravanan S',
 'title':'Technical Leader'
 },
 {
 'id':201,
 'name':'Rajkumar P',
 'title':'Sr Software Engineer'
 }
 ]

def find_employee(employee_id):
  matches = [emp for emp in empDB if emp['id'] == employee_id]
  if len(matches) == 0:
    return None
  return matches[0]

class EmployeeServer(EmployeeService_pb2_grpc.EmployeeServiceServicer):

  def CreateEmployee(self, request, context):
    dat = {
    'id':request.id,
    'name':request.name,
    'title':request.title
    }
    empDB.append(dat)
    return EmployeeService_pb2.StatusReply(status='OK')

  def GetEmployeeDataFromID(self, request, context):
    usr = find_employee(request.id)
    if usr is None:
      context.set_code(grpc.StatusCode.NOT_FOUND)
      context.set_details('Employee not found')
      return EmployeeService_pb2.EmployeeData()

    return EmployeeService_pb2.EmployeeData(id=usr['id'], name=usr['name'], title=usr['title'])

  def UpdateEmployeeTitle(self, request, context):
    usr = find_employee(request.id)
    if usr is None:
      return EmployeeService_pb2.StatusReply(status='NOK')

    usr['title'] = request.title
    return EmployeeService_pb2.StatusReply(status='OK')

  def DeleteEmployee(self, request, context):
    usr = find_employee(request.id)
    if usr is None:
      return EmployeeService_pb2.StatusReply(status='NOK')

    empDB.remove(usr)
    return EmployeeService_pb2.StatusReply(status='OK')

  def ListAllEmployees(self, request, context):
    list = EmployeeService_pb2.EmployeeDataList()
    for item in empDB:
      emp_data = EmployeeService_pb2.EmployeeData(id=item['id'], name=item['name'], title=item['title']) 
      list.employee_data.append(emp_data)
    return list

  def CountEmployees(self, request, context):
    return EmployeeService_pb2.EmployeeCount(count=len(empDB))

  def ListEmployeesByTitle(self, request, context):
    result = EmployeeService_pb2.EmployeeDataList()
    for item in empDB:
      if item['title'].lower() == request.title.lower():
        emp_data = EmployeeService_pb2.EmployeeData(id=item['id'], name=item['name'], title=item['title'])
        result.employee_data.append(emp_data)
    return result

  def UpdateEmployeeName(self, request, context):
    usr = find_employee(request.id)
    if usr is None:
      return EmployeeService_pb2.StatusReply(status='NOK')

    usr['name'] = request.name
    return EmployeeService_pb2.StatusReply(status='OK')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EmployeeService_pb2_grpc.add_EmployeeServiceServicer_to_server(EmployeeServer(), server)
    server.add_insecure_port('[::]:'+const.PORT)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
