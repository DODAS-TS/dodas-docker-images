import cygno as cy
connection = cy.daq_sql_cennection(verbose=False)
def daq_not_on_tape_runs(connection, verbose=False):
    import numpy as np
    sql = "SELECT * FROM `Runlog` WHERE DATEDIFF(`start_time`, CURRENT_TIMESTAMP) \
BETWEEN 0 AND 30 AND `storage_tape_status` < 1 AND `storage_cloud_status` = 1;"
    mycursor = connection.cursor()
    mycursor.execute(sql)
    value = mycursor.fetchall()
    if verbose: print(mycursor.rowcount)
    mycursor.close()
    return np.array(list(zip(*value))[0])
print(daq_not_on_tape_runs(connection))
