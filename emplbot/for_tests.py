import datetime
import pprint
from datetime import datetime as dt
from services.models import Employee, W_table


if __name__ == '__main__':
    test_empl = Employee(f_name='Dmitry', l_name='Stepanov')

    test_empl_info = test_empl.get_info_of_employee()
    print(f'test_empl_info: \n{test_empl_info}')
    test_empl_id = test_empl.get_empl_id()
    print(f'test_empl.get_empl_id():  {test_empl_id}')
    # print(dt.strptime('2022.10.06, 09:00:00', '%Y.%m.%d, %H:%M:%S'))
    start_shift = dt.strptime('2022.10.06, 09:00:00', '%Y.%m.%d, %H:%M:%S')
    end_shift = dt.strptime('2022.10.06, 18:00:00', '%Y.%m.%d, %H:%M:%S')
    shift_time = (end_shift - start_shift)

    # print(test_empl.get_empl_id())

    test_w_table = W_table(
        test_empl_id,
        dt.today(),
        'Hannover',
        'HV-Batterie',
        'Offline programming CPU',
        'Without notes',
        start_shift.time(),
        end_shift.time(),
        shift_time
    )

    # print(test_w_table.start_shift[0], test_w_table.end_shift[0], test_w_table.shift_time[0])
    # test_w_table.add_w_table()
    test_w_day_from = dt.strptime('2022.10.06, 09:00:00', '%Y.%m.%d, %H:%M:%S')
    test_w_day_to = dt.strptime('2022.10.10, 09:00:00', '%Y.%m.%d, %H:%M:%S')
    test_w_table.del_w_day_from = test_w_day_from.date()
    test_w_table.del_w_day_to = test_w_day_to.date()
    test_w_table.delete_w_table()

    # test_w_table.sel_w_day_from = test_w_day_from.date()
    # test_w_table.sel_w_day_to = test_w_day_to.date()
    # test_w_table_info = test_w_table.get_info_of_the_w_days()
    # print(test_w_table_info)