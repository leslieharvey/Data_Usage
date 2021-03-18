class HTMLTemplate:
    """
    This class contains all the information needed to construct an HTML
    template populated with dynamic data.
    """

    top_sub_1 = """
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
    """
    # place section_label here
    top_sub_2 = """
                </h3>
                </td>
            </tr>
            <tr>
                <td colspan="2" style="padding: 0.75pt">
                <p
                    style="font-size: 11pt; font-family: Calibri, sans-serif; margin: 0"
                >
                    <b>
    """
    # place left_justify_label here
    top_sub_3 = """
                    </b>
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
                    <b>
    """
    # place right_justify_label here
    top_sub_4 = """
                    </b>
                </p>
                </td>
            </tr>
    """

    def _create_top_labels(self, section_label, left_justify_label, right_justify_label):
        """
        This function returns a string of the top portion of the HTML template

        Args:
            section_label (str): A string representing the section label of the HTML table
            left_justify_label (str): A string representing the label of the left table column
            right_justify_label (str): A string representing the label of the right table column
        """
        return self.top_sub_1 + section_label + self.top_sub_2 + left_justify_label + self.top_sub_3 + right_justify_label  + self.top_sub_4

    bottom = """
            </tbody>
        </table>
        </div>
    """

    def __create_table_row(self, left_justify, right_justify):
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
        # place left_justify here

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

        # place right_justify here

        row_three = """
            </p>
        </td>
        </tr>
        """

        table_row = row_one + left_justify + row_two + right_justify + row_three

        return table_row

    def __create_data_rows(self, row_data):
        """
        This function returns a string of all the table rows for all the data

        Args:
            row_data (dict): A dictionary containing the data label and value of a row
                The input object has the form::
                        {
                         'data_row': 0.00,
                         'data_row2': 0.00,
                         ...
                        }

        Returns:
            str: A str representing all the specified data table rows
        """
        data_rows_list = []
        for row in row_data:
            html_row = self.__create_table_row(row, str(row_data[row]))
            data_rows_list.append(html_row)

        data_rows_string = ""

        for row in data_rows_list:
            data_rows_string += row

        return data_rows_string

    # cls instead of self (@classmethod)
    def create_html(self, section_label, left_justify_label, right_justify_label, data):
        """
        This function returns a string of all the table rows for all the users

        Args:
            section_label (str): A string representing the section label of the HTML table
            left_justify_label (str): A string representing the label of the left table column
            right_justify_label (str): A string representing the label of the right table column
            data (dict): A dictionary containing the data label and value of a dataset
                The input object has the form::
                        {
                         'data_row': 0.00,
                         'data_row2': 0.00,
                         ...
                        }

        Returns:
            str: A str representing the complete HTML template compiled from dyanmic data
        """
        data_rows = self.__create_data_rows(data)
        return self._create_top_labels(section_label, left_justify_label, right_justify_label) + data_rows + self.bottom