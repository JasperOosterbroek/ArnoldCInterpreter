import io
import unittest
import unittest.mock
import interpeter

class ArithmeticTest(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, StringList, expected_output, mock_stdout):
        interpeter.run(StringList)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_variable_decleration(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP 123\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "";
        self.assert_stdout(StringList, expected_output)

    def test_integer_printing(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "TALK TO THE HAND 123\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "123\n"
        self.assert_stdout(StringList, expected_output)

    def test_negative_integer_printing(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "TALK TO THE HAND -111\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "-111\n"
        self.assert_stdout(StringList, expected_output)

    def test_boolean_printing(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE varfalse\n",
            "YOU SET US UP @I LIED\n",
            "TALK TO THE HAND varfalse\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_string_printing(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "TALK TO THE HAND \"this should be printed\"\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "this should be printed\n"
        self.assert_stdout(StringList, expected_output)

    def test_exotic_string_printing(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "TALK TO THE HAND \"!!! ??? äöäöäöä@#0123=+-,.\"\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "!!! ??? äöäöäöä@#0123=+-,.\n"
        self.assert_stdout(StringList, expected_output)

    def test_integer_declaration_and_printing(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE A\n",
            "YOU SET US UP 999\n",
            "HEY CHRISTMAS TREE B\n",
            "YOU SET US UP 555\n",
            "TALK TO THE HAND A\n",
            "TALK TO THE HAND B\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "999\n555\n"
        self.assert_stdout(StringList, expected_output)

    def test_negative_integer_declaration_and_printing(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE A\n",
            "YOU SET US UP -999\n",
            "HEY CHRISTMAS TREE B\n",
            "YOU SET US UP -555\n",
            "TALK TO THE HAND A\n",
            "TALK TO THE HAND B\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "-999\n-555\n"
        self.assert_stdout(StringList, expected_output)

    def test_assign_single_variable(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION 123\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "123\n"
        self.assert_stdout(StringList, expected_output)

    def test_assign_multiple_variables(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP 22\n",
            "HEY CHRISTMAS TREE var2\n",
            "YOU SET US UP 27\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION 123\n",
            "ENOUGH TALK\n",
            "GET TO THE CHOPPER var2\n",
            "HERE IS MY INVITATION 707\n",
            "ENOUGH TALK\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION var2\n",
            "GET UP var\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "830\n"
        self.assert_stdout(StringList, expected_output)

    def test_increment_variable(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "GET UP 44\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "66\n"
        self.assert_stdout(StringList, expected_output)

    def test_decrement_variable(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "GET DOWN 44\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "-22\n"
        self.assert_stdout(StringList, expected_output)

    def test_decrement_by_negative_value(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "GET DOWN -44\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "66\n"
        self.assert_stdout(StringList, expected_output)


    def test_increment_by_negative_value(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "GET UP -44\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "-22\n"
        self.assert_stdout(StringList, expected_output)

    def test_multiply_variables(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "YOU'RE FIRED 13\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "286\n"
        self.assert_stdout(StringList, expected_output)

    def test_multiply_variables_different_signs(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "YOU'RE FIRED -13\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "-286\n"
        self.assert_stdout(StringList, expected_output)

    def test_multiply_variables_with_zero(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "YOU'RE FIRED 0\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_multiply_assigned_variables(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 7\n",
            "HEY CHRISTMAS TREE VAR2\n",
            "YOU SET US UP 4\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "YOU'RE FIRED VAR2\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "28\n"
        self.assert_stdout(StringList, expected_output)

    def test_variable_dividing(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 100\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "HE HAD TO SPLIT 4\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "25\n"
        self.assert_stdout(StringList, expected_output)

    def test_variable_dividing_different_signs(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 99\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "HE HAD TO SPLIT -33\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "-3\n"
        self.assert_stdout(StringList, expected_output)

    def test_divide_with_one(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION VAR\n",
            "HE HAD TO SPLIT 1\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "22\n"
        self.assert_stdout(StringList, expected_output)

    def test_calculating_modulo_var_1(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP 1\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION var\n",
            "I LET HIM GO 2\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_calculating_modulo_var_2(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP 2\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION var\n",
            "I LET HIM GO 2\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_different_arithmetic_operations_1(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION 11\n",
            "GET DOWN 43\n",
            "GET UP 54\n",
            "GET UP 44\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "66\n"
        self.assert_stdout(StringList, expected_output)

    def test_different_arithmetic_operations_2(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION 11\n",
            "GET DOWN 55\n",
            "GET UP 11\n",
            "GET UP 22\n",
            "GET UP 23\n",
            "GET DOWN 0\n",
            "GET UP 0\n",
            "GET UP 1\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "13\n"
        self.assert_stdout(StringList, expected_output)

    def test_different_arithmetic_operations_3(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "GET TO THE CHOPPER VAR\n",
            "HERE IS MY INVITATION 11\n",
            "GET DOWN 22\n",
            "HE HAD TO SPLIT -11\n",
            "YOU'RE FIRED 23\n",
            "GET UP 23\n",
            "GET DOWN 22\n",
            "HE HAD TO SPLIT 2\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND VAR\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "12\n"
        self.assert_stdout(StringList, expected_output)

    def test_duplicate_variables_declaration(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "HEY CHRISTMAS TREE VAR\n",
            "YOU SET US UP 22\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "[Parse Error: Multiple declerations of VAR on line 3, Parse Error: Multiple declerations of VAR on line 3]\n"
        self.assert_stdout(StringList, expected_output)

    def test_invalid_argument_names(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE 1VAR\n",
            "YOU SET US UP 123\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "[Syntax Error: Invalid argument \"1VAR\" on line 2]\n"
        self.assert_stdout(StringList, expected_output)

class LogicalTest(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, StringList, expected_output, mock_stdout):
        interpeter.run(StringList)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_false_or_true_evaluate_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP 0\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION 0\n",
            "CONSIDER THAT A DIVORCE 1\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_or_false_evaluate_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @NO PROBLEMO\n",
            "CONSIDER THAT A DIVORCE @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_or_true_evaluate_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @NO PROBLEMO\n",
            "CONSIDER THAT A DIVORCE @NO PROBLEMO\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_false_or_false_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @I LIED\n",
            "CONSIDER THAT A DIVORCE @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_false_and_true_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @I LIED\n",
            "KNOCK KNOCK @NO PROBLEMO\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_and_false_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @NO PROBLEMO\n",
            "KNOCK KNOCK @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_and_false_evaluate_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @NO PROBLEMO\n",
            "KNOCK KNOCK @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_and_true_evaluate_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @NO PROBLEMO\n",
            "KNOCK KNOCK @NO PROBLEMO\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_and_true_and_false_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION 1\n",
            "KNOCK KNOCK 1\n",
            "KNOCK KNOCK 0\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_and_true_and_true_and_false_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @NO PROBLEMO\n",
            "KNOCK KNOCK @NO PROBLEMO\n",
            "KNOCK KNOCK @NO PROBLEMO\n",
            "KNOCK KNOCK @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_and_true_and_true_and_true_and_false_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @NO PROBLEMO\n",
            "KNOCK KNOCK @NO PROBLEMO\n",
            "KNOCK KNOCK @NO PROBLEMO\n",
            "KNOCK KNOCK @NO PROBLEMO\n",
            "KNOCK KNOCK @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_false_or_false_or_false_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @I LIED\n",
            "CONSIDER THAT A DIVORCE @I LIED\n",
            "CONSIDER THAT A DIVORCE @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_false_or_true_and_false_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @I LIED\n",
            "CONSIDER THAT A DIVORCE @NO PROBLEMO\n",
            "KNOCK KNOCK @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_false_and_false_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION @I LIED\n",
            "KNOCK KNOCK @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_false_equals_false_evaluate_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE varfalse\n",
            "YOU SET US UP @I LIED\n",
            "HEY CHRISTMAS TREE varfalse2\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER varfalse\n",
            "HERE IS MY INVITATION @I LIED\n",
            "YOU ARE NOT YOU YOU ARE ME varfalse2\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND varfalse\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_equals_false_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE varfalse\n",
            "YOU SET US UP @I LIED\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION @NO PROBLEMO\n",
            "YOU ARE NOT YOU YOU ARE ME varfalse\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_true_equals_true_equals_true_evaluates_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION @NO PROBLEMO\n",
            "YOU ARE NOT YOU YOU ARE ME @NO PROBLEMO\n",
            "YOU ARE NOT YOU YOU ARE ME @NO PROBLEMO\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_13_equals_13_equals_true_evaluates_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION 13\n",
            "YOU ARE NOT YOU YOU ARE ME 13\n",
            "YOU ARE NOT YOU YOU ARE ME @NO PROBLEMO\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_13_equals_14_equals_false_evaluate_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION 13\n",
            "YOU ARE NOT YOU YOU ARE ME 14\n",
            "YOU ARE NOT YOU YOU ARE ME @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_1_equals_2_equals_3_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION 1\n",
            "YOU ARE NOT YOU YOU ARE ME 2\n",
            "YOU ARE NOT YOU YOU ARE ME 3\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_13_equals_13_equals_14_evaluates_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION 13\n",
            "YOU ARE NOT YOU YOU ARE ME 13\n",
            "YOU ARE NOT YOU YOU ARE ME 14\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_1_equals_2_evaluates_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE one\n",
            "YOU SET US UP 1\n",
            "HEY CHRISTMAS TREE two\n",
            "YOU SET US UP 2\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @NO PROBLEMO\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION one\n",
            "YOU ARE NOT YOU YOU ARE ME two\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_2_greater_1_evaluates_true(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE one\n",
            "YOU SET US UP 1\n",
            "HEY CHRISTMAS TREE two\n",
            "YOU SET US UP 2\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @NO PROBLEMO\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION two\n",
            "LET OFF SOME STEAM BENNET one\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n"
        self.assert_stdout(StringList, expected_output)

    def test_1_greater_2_evaluate_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE one\n",
            "YOU SET US UP 1\n",
            "HEY CHRISTMAS TREE two\n",
            "YOU SET US UP 2\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @NO PROBLEMO\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION one\n",
            "LET OFF SOME STEAM BENNET two\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_3_greater_3_evaluates_false(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE three\n",
            "YOU SET US UP 3\n",
            "HEY CHRISTMAS TREE three2\n",
            "YOU SET US UP 3\n",
            "HEY CHRISTMAS TREE result\n",
            "YOU SET US UP @NO PROBLEMO\n",
            "GET TO THE CHOPPER result\n",
            "HERE IS MY INVITATION three\n",
            "LET OFF SOME STEAM BENNET three2\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND result\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "0\n"
        self.assert_stdout(StringList, expected_output)

    def test_faulty_logic(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "RIGHT? WRONG! VAR\n",
            "YOU SET US UP @I LIED\n",
            "GET TO THE CHOPPER VAR\n",
            "@I LIED\n",
            "@I LIED\n",
            "CONSIDER THAT A DIVORCE\n",
            "@NO PROBLEMO\n",
            "ENOUGH TALK\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "[Syntax Error: Invalid syntax RIGHT? WRONG! VAR on line 3, Syntax Error: missing argument after \"@I LIED\" on line 5, Syntax Error: missing argument after \"@I LIED\" on line 6, Syntax Error: missing argument after \"CONSIDER THAT A DIVORCE\" on line 7, Syntax Error: missing argument after \"@NO PROBLEMO\" on line 8]\n"
        self.assert_stdout(StringList, expected_output)

class MethodTest(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, StringList, expected_output, mock_stdout):
        interpeter.run(StringList)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_evaluate_method_other_than_main(self):
        StringList = [
            "LISTEN TO ME VERY CAREFULLY mymethod\n",
            "HASTA LA VISTA, BABY\n",
            "IT'S SHOWTIME\n",
            "TALK TO THE HAND \"Hello\"\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "Hello\n"
        self.assert_stdout(StringList, expected_output)

    def test_evaluate_method_other_than_main2(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "TALK TO THE HAND \"Hello\"\n",
            "YOU HAVE BEEN TERMINATED\n",
            "LISTEN TO ME VERY CAREFULLY mymethod\n",
            "HASTA LA VISTA, BABY\n"
        ]
        expected_output = "Hello\n"
        self.assert_stdout(StringList, expected_output)

class BranchTest(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, StringList, expected_output, mock_stdout):
        interpeter.run(StringList)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_simple_if_statement(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE vartrue\n",
            "YOU SET US UP @NO PROBLEMO\n",
            "BECAUSE I'M GOING TO SAY PLEASE vartrue\n",
            "TALK TO THE HAND \"this branch should be reached\"\n",
            "YOU HAVE NO RESPECT FOR LOGIC\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "this branch should be reached\n"
        self.assert_stdout(StringList, expected_output)

    def test_simple_if_statement_2(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE vartrue\n",
            "YOU SET US UP @I LIED\n",
            "BECAUSE I'M GOING TO SAY PLEASE vartrue\n",
            "TALK TO THE HAND \"this branch should not be reached\"\n",
            "YOU HAVE NO RESPECT FOR LOGIC\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = ""
        self.assert_stdout(StringList, expected_output)

    def test_simple_if_else(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE vartrue\n",
            "YOU SET US UP @NO PROBLEMO\n",
            "BECAUSE I'M GOING TO SAY PLEASE vartrue\n",
            "TALK TO THE HAND \"this branch should be reached\"\n",
            "BULLSHIT\n",
            "TALK TO THE HAND \"this branch should not be reached\"\n",
            "YOU HAVE NO RESPECT FOR LOGIC\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "this branch should be reached\n"
        self.assert_stdout(StringList, expected_output)

    def test_simple_if_else_2(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE varfalse\n",
            "YOU SET US UP @I LIED\n",
            "BECAUSE I'M GOING TO SAY PLEASE varfalse\n",
            "TALK TO THE HAND \"this branch should not be reached\"\n",
            "BULLSHIT\n",
            "TALK TO THE HAND \"this branch should be reached\"\n",
            "YOU HAVE NO RESPECT FOR LOGIC\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "this branch should be reached\n"
        self.assert_stdout(StringList, expected_output)

    def test_assign_variable_in_if(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE var\n",
            "YOU SET US UP 0\n",
            "HEY CHRISTMAS TREE vartrue\n",
            "YOU SET US UP @NO PROBLEMO\n",
            "BECAUSE I'M GOING TO SAY PLEASE vartrue\n",
            "GET TO THE CHOPPER var\n",
            "HERE IS MY INVITATION 3\n",
            "ENOUGH TALK\n",
            "YOU HAVE NO RESPECT FOR LOGIC\n",
            "TALK TO THE HAND var\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "3\n"
        self.assert_stdout(StringList, expected_output)

    def test_stub_while(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE varfalse\n",
            "YOU SET US UP @I LIED\n",
            "STICK AROUND varfalse\n",
            "CHILL\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = ""
        self.assert_stdout(StringList, expected_output)

    def test_stub_while_2(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "STICK AROUND @I LIED\n",
            "CHILL\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = ""
        self.assert_stdout(StringList, expected_output)

    def test_while_executed_once(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE varfalse\n",
            "YOU SET US UP @NO PROBLEMO\n",
            "STICK AROUND varfalse\n",
            "GET TO THE CHOPPER varfalse\n",
            "HERE IS MY INVITATION @I LIED\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND \"while statement printed once\"\n",
            "CHILL\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "while statement printed once\n"
        self.assert_stdout(StringList, expected_output)

    def test_while_executed_consquently(self):
        StringList = [
            "IT'S SHOWTIME\n",
            "HEY CHRISTMAS TREE isLessThan10\n",
            "YOU SET US UP @NO PROBLEMO\n",
            "HEY CHRISTMAS TREE n\n",
            "YOU SET US UP 0\n",
            "STICK AROUND isLessThan10\n",
            "GET TO THE CHOPPER n\n",
            "HERE IS MY INVITATION n\n",
            "GET UP 1\n",
            "ENOUGH TALK\n",
            "TALK TO THE HAND n\n",
            "GET TO THE CHOPPER isLessThan10\n",
            "HERE IS MY INVITATION 10\n",
            "LET OFF SOME STEAM BENNET n\n",
            "ENOUGH TALK\n",
            "CHILL\n",
            "YOU HAVE BEEN TERMINATED\n"
        ]
        expected_output = "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n"
        self.assert_stdout(StringList, expected_output)

if __name__ == '__main__':
    unittest.main()