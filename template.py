class HTMLTemplate:
    """
    This class contains all the information needed to construct an HTML
    template populated with dynamic data.
    """

    top = """
    <div lang="en-US" link="blue" vlink="purple" style="word-wrap: break-word">
    <p style="font-size: 11pt; font-family: Calibri, sans-serif; margin: 0">
        <span style="display: none">&nbsp;</span>
    </p>
    <table border="0" cellspacing="3" cellpadding="0" style="width: 70%">
        <tbody>
        <tr>
            <td colspan="3" style="padding: 0.75pt">
            <h3
                align="center"
                style="
                font-size: 13.5pt;
                font-family: Calibri, sans-serif;
                font-weight: bold;
                text-align: center;
                margin-right: 0;
                margin-left: 0;
                "
            >
                Member Usage
            </h3>
            </td>
        </tr>
        <tr>
            <td colspan="2" style="padding: 0.75pt">
            <p
                style="font-size: 11pt; font-family: Calibri, sans-serif; margin: 0"
            >
                <b>Username</b>
            </p>
            </td>
            <td style="padding: 0.75pt">
            <p
                align="right"
                style="
                font-size: 11pt;
                font-family: Calibri, sans-serif;
                text-align: right;
                margin: 0;
                "
            >
                <b>Quota Used (GB)</b>
            </p>
            </td>
        </tr>
    """

    bottom = """
        </tbody>
    </table>
    </div>
    """

    def __init__(self):
        super()

    def __create_table_row(self, username, usage):
        """
        This function returns a string of a table row for an indivual user.

        Args:
            username (str): The username to be entered in the table row
            usage (str): The usage (GB) to be entered in the table row

        Returns:
            str: A str representing a table row
        """
        row_one = """
        <tr>
        <td colspan="2" style="padding: 0.75pt">
            <p style="font-size: 11pt; font-family: Calibri, sans-serif; margin: 0">
        """
        # place username here

        row_two = """
            </p>
        </td>
        <td style="padding: 0.75pt">
            <p
            align="right"
            style="
                font-size: 11pt;
                font-family: Calibri, sans-serif;
                text-align: right;
                margin: 0;
            "
            >
        """

        # place usage here

        row_three = """
            </p>
        </td>
        </tr>
        """

        table_row = row_one + username + row_two + usage + row_three

        return table_row

    def __create_user_rows(self, user_data):
        """
        This function returns a string of all the table rows for all the users

        Args:
            user_data (dict): A dictionary containing the username and usage of a user
                The input object has the form::
                        {
                         'username': 0.00,
                         'username2': 0.00,
                         ...
                        }

        Returns:
            str: A str representing all the specified user table rows
        """
        user_rows_list = []
        for user in user_data:
            row = self.__create_table_row(user, str(user_data[user]))
            user_rows_list.append(row)

        user_rows_string = ""

        for row in user_rows_list:
            user_rows_string += row

        return user_rows_string

    # cls instead of self (@classmethod)
    def create_html(self, data):
        """
        This function returns a string of all the table rows for all the users

        Args:
            data (dict): A dictionary containing the username and usage of a user
                The input object has the form::
                        {
                         'username': 0.00,
                         'username2': 0.00,
                         ...
                        }

        Returns:
            str: A str representing the complete HTML template compiled from dyanmic data
        """
        user_rows = self.__create_user_rows(data)
        return self.top + user_rows + self.bottom