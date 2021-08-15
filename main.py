import sqlite3
import time
from sqlite3 import Error
from webwhatsapi import WhatsAPIDriver


def connect_to_db(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def insert_into_chats(conn, cid):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    try:
        sql = "INSERT INTO chat_id(chat_id) VALUES(?)"
        cur = conn.cursor()
        cur.execute(sql, (cid,))
        conn.commit()
        return True

    except sqlite3.Error:
        return False


def print_contacts_id():
    driver = WhatsAPIDriver(loadstyles=True)
    print("Waiting for QR")
    driver.wait_for_login()
    print("Bot started")
    for chat in driver.get_all_chats():
        print(chat)
    driver.close()


def run_bot(wgroup_id, wmessage):

    driver = WhatsAPIDriver(loadstyles=True)
    driver.wait_for_login()
    conn = connect_to_db("contacts.db")
    while True:
        time.sleep(3)
        #print("checking for new members")
        for cid in driver.group_get_participants_ids(wgroup_id):
            if insert_into_chats(conn, str(cid["user"])):
                print("sending message to "+str(cid))
                chat_status = driver.check_number_status(cid['user'])
                if chat_status.status == 404:
                    print("Creating contact for number "+str(cid))
                    print("chat : "+str(driver.get_chat_from_phone_number(cid['user'], True)))
                    print("unblocking contact "+str(driver.contact_unblock(cid)))
                print("Message status "+str(driver.send_message_to_id(cid, wmessage)))
                print("")
    driver.close()


def send_test_message(test_id, test_message):
    driver = WhatsAPIDriver(loadstyles=True)
    driver.wait_for_login()
    driver.send_message_to_id(test_id, test_message)
    driver.close()

if __name__ == "__main__":
    message = "Hello line 1"
    message += "\n" + "Hello Line 2"
    group_id = "Group ID@g.us"
    run_bot(group_id, message)
    #print_contacts_id()