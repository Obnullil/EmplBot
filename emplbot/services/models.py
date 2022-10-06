from connections import cursor_command


class Employee:
    def __init__(self, f_name, l_name, company='', specialty='', email='', phone=''):
        self.__employee_id = 0,
        self.f_name = f_name,
        self.l_name = l_name,
        self.company = company,
        self.specialty = specialty,
        self.email = email,
        self.phone = phone,
        self.__sql_command = '',
        self.__sql_param = ()

    def get_empl_id(self):
        return self.__employee_id

    def init_empl_id(self):
        self.__employee_id = 0

    def add_employee(self):
        self.__sql_command = """INSERT INTO employee (
                                f_name,
                                l_name,
                                company,
                                specialty,
                                email,
                                phone) VALUES (%s, %s, %s, %s, %s, %s)"""
        self.__sql_param = (self.f_name, self.l_name, self.company, self.specialty, self.email, self.phone)

        cursor_command('add', self.__sql_command, self.__sql_param)

    def delete_employee(self):
        if self.__employee_id != 0:
            self.__sql_command = """DELETE FROM employee WHERE employee_id = %s"""
            self.__sql_param = (self.__employee_id, )

            cursor_command('del', self.__sql_command, self.__sql_param)
        else:
            print('[INFO] We have no user with employee_id = 0')

    def get_info_of_employee(self):
        self.__sql_command = """SELECT * FROM employee WHERE f_name = %s AND l_name = %s"""
        self.__sql_param = (self.f_name, self.l_name)

        empl_info = cursor_command('get', self.__sql_command, self.__sql_param)
        # print(f'empl_info: {empl_info[0][0]}')
        # print(self.__employee_id)
        if self.__employee_id == 0:
            self.__employee_id = empl_info[0][0]




if __name__ == '__main__':
    test_empl = Employee(f_name='Dmitry', l_name='Stepanov')
    test_empl.add_employee()
