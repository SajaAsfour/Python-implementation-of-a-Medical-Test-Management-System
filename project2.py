                    #saja asfour 1210737 sec 4
                    #shahed shreteh 1210444 sec 7
                    #python project - project #2
#------------------------------------------------------------------#
import re
from datetime import datetime
import csv

#This class stores information about a medical test definition,
# including its name, range (minimum and maximum), unit of measurement, and test code
class MedicalTestDefinition:
    def __init__(self, name, range_min, range_max, unit, turnaround_time):
        self.name = name                            # name of medical test
        self.range_min = range_min                  # minimum range of medical test
        self.range_max = range_max                  # maximum range of medical test
        self.unit = unit                            # unit of test
        self.turnaround_time = turnaround_time      # Time taken to get test results in DD-HH-MM format

class Patient:
    # dictionary to store all patients with patient_id as the key
    all_patients = {}

    def __init__(self, patient_id):
        self.patient_id = patient_id                # Unique identifier for the patient
        self.records = []                           # List to store medical test records for this patient
        Patient.all_patients[patient_id] = self     # Add this patient to the dictionary

    # Add a medical test record to the patient's records
    def add_record(self, record):
        self.records.append(record)

    def __str__(self):
        # String representation of the patient
        return f"Patient ID: {self.patient_id}, Records: {len(self.records)}"


#Class to manage medical test definitions and interact with the user
class MedicalTestSystem:
    #Initialize the MedicalTestSystem with the files path where medical test definitions and nedical record  stored
    def __init__(self):
        self.medical_tests_file = "medicalTest.txt"         # File to store medical test definitions
        self.medical_records_file = "midecalRecord.txt"     # File to store patient medical records
        self.patients = self.load_medical_records()         # Load patient medical records from the file

        # Initialize the normal_ranges attribute
        self.normal_ranges = {}

    # Load medical records for patients from a file
    def load_medical_records(self):
        #define dictonary to store the data from file
        patients = {}
        try:
            #opern the file for read
            with open(self.medical_records_file, "r") as file:
                #itterate each line in the file
                for line in file:
                    #split the line into parts one for id and other for details
                    parts = line.strip().split(': ', 1)
                    if len(parts) == 2:
                        patient_id = parts[0].strip()
                        #split part2 which is the details by comma
                        details = parts[1].split(', ')

                        if len(details) >= 5:
                            #parts of part 1 ( details)
                            test_name = details[0].strip()
                            test_date_time = details[1].strip()
                            result_value = details[2].strip()
                            unit = details[3].strip()
                            status = details[4].strip()
                            #this is used just for completed status
                            results_date_time = details[5].strip() if len(details) > 5 else None

                            # Validate date and time formats
                            if not self.validate_datetime(test_date_time):
                                print(f"invalid test date and time format: {line.strip()}")
                                continue
                            if results_date_time and not self.validate_datetime(results_date_time):
                                print(f"invalid results date and time format: {line.strip()}")
                                continue

                            #dictonary for details
                            record = {
                                'test_name': test_name,
                                'test_date_time': test_date_time,
                                'result_value': result_value,
                                'unit': unit,
                                'status': status,
                                'results_date_time': results_date_time
                            }

                            # Add record to the corresponding patient
                            #Check if the patient-id already exists in the dictionary
                            #If the patient_id is not found in the dictionary,
                            # a new Patient object is created using the patient_id and added to the patients dictionary
                            if patient_id not in patients:
                                patients[patient_id] = Patient(patient_id)
                            #initializes a new instance of the Patient class, likely using the patient_id as an identifier for that instance
                            patients[patient_id].add_record(record)
        #if the file does not exist
        except FileNotFoundError:
            print(f"{self.medical_records_file} not found! So No records loaded :(")
        return patients

    #Validate that the given value can be converted to a float
    def validate_numeric(self, value):
        #return True if the value is numeric, False otherwise
        try:
            float(value)
            return True
        except ValueError:
            return False

    # Validate the format of the turnaround time
    def validate_turnaround_time(self, time_str):
        # Validate the turnaround time format as dd-hh-mm
        return re.fullmatch(r'\d{2}-\d{2}-\d{2}', time_str)

    # Validate the format of a date-time string
    def validate_datetime(self, datetime_str):
            try:
                datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                return True
            except ValueError:
                return False

    #Validate the format date string
    def validate_date(self,date):
        try:
            datetime.strptime(date,'%Y-%m-%d')
            return  True
        except ValueError:
            return False

    # Validate the format of the patient ID
    def validate_patient_id(self, patient_id):
            return re.fullmatch(r'\d{7}', patient_id)

        # Validate the status of the medical test
    def validate_status(self, status):
            return status in ['Pending', 'Completed', 'Reviewed','pending' ,'completed' ,'reviewed']


    def add_new_medical_test_definition(self):

        # get the test details from user input
        name = input("Enter Test Name : ")

        # Check if the test name already exists
        if self.test_name_exists(name):
            print(f"Medical test '{name}' already exists! Please enter a new test :)")
            return

        # get and validate the minimum range value (if provided)
        range_min = input("Enter Minimum Range (leave empty if N/A): ")
        if range_min and not self.validate_numeric(range_min):
            print("Invalid minimum range ! It must be a number or empty")
            return

        # get and validate the maximum range value (if provided)
        range_max = input("Enter Maximum Range (leave empty if N/A): ")
        if range_max and not self.validate_numeric(range_max):
            print("Invalid maximum range ! It must be a number or empty")
            return

        # get the unit of measurement for the test
        unit = input("Enter Unit of Measurement: ")

        # get and validate the turnaround time in DD-hh-mm format
        turnaround_time = input("Enter Turnaround Time (format: DD-HH-MM): ")
        if not self.validate_turnaround_time(turnaround_time):
            print("Invalid turnaround time format! Please follow DD-HH-MM")
            return

        # Create the medical test definition object with the  information
        medical_test_definition = MedicalTestDefinition(name, range_min, range_max, unit, turnaround_time)

        # Save the test definition to the file
        self.save_medical_test_definition(medical_test_definition)

        # conforming meesage
        print(f"Medical test '{name}' added successfully :)")

    # Check if a medical test name already exists in the medicalTests.txt file
    def test_name_exists(self, name):
        try:
            #open the medicalTest file for read data
            with open(self.medical_tests_file, "r") as file:
                for line in file:
                    #check if this name exist in the file , return true if exist
                    if line.startswith(f"Name: {name};"):
                        return True
        #File does not exist yet ( no tests have been saved )
        except FileNotFoundError:
            return False
        return False

    #save to midecal Record
    def save_medical_record(self, patient_id, record):
        #open file
        with open(self.medical_records_file, "a") as file:
            #string for each medical record
            entry = f"{patient_id}: {record['test_name']}, {record['test_date_time']}, {record['result_value']}, {record['unit']}, {record['status']}"
            #this for completed status
            if record['results_date_time']:
                entry += f", {record['results_date_time']}"
            #write record to the file
            file.write(entry + "\n")

    # Save the medical test definition to the medicalTest.txt file in the specified format
    def save_medical_test_definition(self, medical_test_definition):
            # Prepare the range string if the range values are provided
            Range = f"Range:"
            range_str1 = f" > {medical_test_definition.range_min}" if medical_test_definition.range_min else ""
            range_str2 = f", < {medical_test_definition.range_max}" if medical_test_definition.range_max else ""
            # Prepare the full entry in the required format
            entry = (f"Name: {medical_test_definition.name}; {Range}{range_str1}{range_str2}; Unit: {medical_test_definition.unit}; "
                     f"{medical_test_definition.turnaround_time}")

            # Append the new entry to the medicalTests.txt file
            with open(self.medical_tests_file, "a") as file:
                file.write(entry + "\n")

    # Get details of a new medical test record from the user, validate the inputs, and save the record
    def add_new_medical_test_record(self):
        patient_id = input("Enter Patient ID (7 digits): ")
        #check validation of ID
        if not self.validate_patient_id(patient_id):
            print("Invalid Patient ID. It must be exactly 7 digits.")
            return

        test_name = input("Enter Test Name: ")

        test_date_time = input("Enter Test Date and Time (format: YYYY-MM-DD HH:mm): ")
        #check validation for datetime
        if not self.validate_datetime(test_date_time):
            print("Invalid test date and time format.")
            return

        result_value = input("Enter Result Value: ")
        #check tvalidation for result
        if not self.validate_numeric(result_value):
            print("Invalid result value. It must be a number.")
            return

        unit = input("Enter Unit of Measurement: ")

        status = input("Enter Status (Pending, Completed, Reviewed): ")
        #check validation for status
        if not self.validate_status(status):
            print("Invalid status. It must be 'Pending', 'Completed', or 'Reviewed'.")
            return

        # this for completed status
        results_date_time = None
        if status.lower() == 'completed':
            results_date_time = input("Enter Results Date and Time (format: YYYY-MM-DD HH:mm): ")
            if not self.validate_datetime(results_date_time):
                print("Invalid results date and time format.")
                return

        record = {
            'test_name': test_name,
            'test_date_time': test_date_time,
            'result_value': result_value,
            'unit': unit,
            'status': status,
            'results_date_time': results_date_time
        }

        #if the id exist , then add the new test for it
        if patient_id in self.patients:
            self.patients[patient_id].add_record(record)
        else:
            #create new object
            new_patient = Patient(patient_id)
            new_patient.add_record(record)
            self.patients[patient_id] = new_patient

        #this for write the medical test inside the file
        self.save_medical_record(patient_id, record)

        #conformied message
        print(f"Medical test record for Patient ID '{patient_id}' added successfully.")

    # Save all patients medical records back to the file
    def save_medical_records_to_file(self):
                with open(self.medical_records_file, "w") as file:
                    for patient_id, patient in self.patients.items():
                        for record in patient.records:
                            entry = f"{patient_id}: {record['test_name']}, {record['test_date_time']}, {record['result_value']}, {record['unit']}, {record['status']}"
                            if record['status'].lower() == 'completed' and record['results_date_time']:
                                entry += f", {record['results_date_time']}"
                            file.write(entry + "\n")

    # update an existing medical test record for a patient
    def update_medical_test_record(self):
                patient_id = input("Enter Patient ID (7 digits): ")

                #ensure the validity of patient_id
                if not self.validate_patient_id(patient_id):
                    print("Invalid Patient ID. It must be exactly 7 digits.")
                    self.update_medical_test_record()
                    return

                #check if the id is in the records test or not
                if patient_id not in self.patients:
                    print(f"No records found for Patient ID: {patient_id}")
                    self.update_medical_test_record()
                    return

                # List all records for the patient and allow selection
                patient = self.patients[patient_id]
                # here we used 'enumerate' which is function in Python is a built-in function that adds a counter to an iterable
                # (like a list, tuple, or string) and returns it as an enumerate object.
                # This object can then be used directly in a loop or converted to a list of tuples containing pairs of index and value.
                for i, record in enumerate(patient.records, start=1):
                    print(f"{i}. {record['test_name']} on {record['test_date_time']} - Status: {record['status']}")

                try:
                    # Get the user's choice for which record to update
                    choice = int(input("Enter the number of the test record you want to update: ")) - 1 # -1 becouse enumerate start from 0
                    #check the valid for choice
                    if choice < 0 or choice >= len(patient.records):
                        print("Invalid choice! Please select a valid record number!")
                        return

                # if user enter anything that is not a number
                except ValueError:
                    print("Invalid input! Please enter a number!")
                    return

                # Get the selected record
                record = patient.records[choice]

                #this function to let user enter data and check the validation
                def enterdata():
                    # Allow the user to update specific fields
                    print("Leave the field blank if you do not want to change it :)")
                    new_test_name = input(f"Enter new Test Name (current: {record['test_name']}): ").strip()
                    if new_test_name:
                        record['test_name'] = new_test_name

                    new_test_date_time = input(f"Enter new Test Date and Time (format: YYYY-MM-DD HH:mm) (current: {record['test_date_time']}): ").strip()
                    #check the validation for test date and time
                    if new_test_date_time:
                        if self.validate_datetime(new_test_date_time ):
                            record['test_date_time'] = new_test_date_time

                        else:
                            print("date time is invalid , try again")
                            return enterdata()
                    new_result_value = input(f"Enter new Result Value (current: {record['result_value']}): ").strip()
                    #check validation for result
                    if new_result_value :
                        if self.validate_numeric(new_result_value):
                            record['result_value'] = new_result_value
                        else:
                            print("result must be number , try again")
                            return enterdata()

                    new_unit = input(f"Enter new Unit of Measurement (current: {record['unit']}): ").strip()
                    if new_unit:
                        record['unit'] = new_unit
                    new_status = input(f"Enter new Status (Pending, Completed, Reviewed) (current: {record['status']}): ").strip()
                    #check validation for status
                    if new_status :
                        if self.validate_status(new_status):
                            record['status'] = new_status
                        else:
                            print("Status must be Completed ,Reviewed or Pending")
                            return enterdata()
                        # Update results date time if status is completed
                        if new_status.lower() == 'completed':
                            new_results_date_time = input(f"Enter new Results Date and Time (format: YYYY-MM-DD HH:mm) (current: {record.get('results_date_time', 'N/A')}): ").strip()
                            if new_results_date_time :
                                if self.validate_datetime(new_results_date_time):
                                    record['results_date_time'] = new_results_date_time
                                else:
                                    print("invalid date it must be YYYY-MM-DD HH-MM")
                                    return enterdata()

                    # Save the updated record back to the file
                    self.save_medical_records_to_file()
                enterdata()
                #conformied message
                print("Medical test record updated successfully.")

    #function to update the medical test definition
    def update_medical_test_definition(self):
        # Load all medical tests from the file into a list
        medical_tests = []
        try:
            with open(self.medical_tests_file, "r") as file:
                for line in file:
                    medical_tests.append(line.strip())
        except FileNotFoundError:
            print(f"{self.medical_tests_file} not found! No tests available to update :(")
            return

        # Display all available medical tests to the user
        if not medical_tests:
            print("No medical tests available for updating :(")
            return

        print("\nAvailable Medical Tests:")
        for i, test in enumerate(medical_tests, start=1):
            # Show the test name
            print(f"{i}. {test.split(';')[0]}")

        # Ask the user which test they want to update
        choice = input("Enter the number of the medical test you want to update: ")
        #validate the number that user enter
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(medical_tests):
            print("Invalid choice! Please enter a valid number :)")
            return

        #to start from 0
        index = int(choice) - 1
        selected_test = medical_tests[index]
        print(f"Selected Test: {selected_test}")

        # Ask the user which fields they want to update from the test that chosen
        #split the line into two parts
        parts = selected_test.split(';')
        #split part one to get thw test name
        test_name = parts[0].split(': ')[1]
        #split part two to get the minumum and maximum range
        range_part = parts[1].split('Range:')[1].strip()
        unit = parts[2].split('Unit: ')[1].strip()
        turnaround_time = parts[3].strip()
        minRange=range_part.split(', ')[0].strip('> ')
        maxRange=range_part.split(', ')[1].strip('< ')
        print("\nLeave any field empty if you do not want to update it :)")
        new_name = input(f"Enter new Test Name (current: {test_name}): ")  or test_name
        new_range_min = input(f"Enter new Minimum Range (current: {minRange}): ") or minRange
        new_range_max = input(f"Enter new Maximum Range (current: {maxRange}): ") or maxRange
        new_unit = input(f"Enter new Unit (current: {unit}): ") or unit
        new_turnaround_time = input(f"Enter new Turnaround Time (current: {turnaround_time}): ") or turnaround_time

        # Validate the inputs
        if new_range_min and not self.validate_numeric(new_range_min):
            print("Invalid minimum range! It must be a number or empty!")
            return

        if new_range_max and not self.validate_numeric(new_range_max):
            print("Invalid maximum range! It must be a number or empty!")
            return

        if new_range_max < new_range_min :
            print("select range correctly")

        if not self.validate_turnaround_time(new_turnaround_time):
            print("Invalid turnaround time format! Please follow DD-HH-MM")
            return

        # Update the selected test with new values
        updated_test = (
            f"Name: {new_name}; Range: > {new_range_min}, < {new_range_max}; Unit: {new_unit}; "
            f"{new_turnaround_time}"
        )

        medical_tests[index] = updated_test

        # Save the updated tests back to the file
        with open(self.medical_tests_file, "w") as file:
            for test in medical_tests:
                file.write(test + "\n")
        #conformied message
        print(f"Medical test '{new_name}' updated successfully.")

    #this function to load range and get the normal from it
    def load_normal_ranges(self):
        # Load the normal ranges for each test from the test data file
        self.normal_ranges = {}

        # Read the test data line by line
        with open('medicalTest.txt', 'r') as file:
            for line in file:
                # Strip whitespace from the line and split it by semicolons
                parts = line.strip().split(";")

                # Initialize variables for test name, min_range, and max_range
                test_name = None
                min_range = None
                max_range = None

                # Iterate through each part of the split line
                for part in parts:
                    # Remove any leading/trailing whitespace
                    part = part.strip()

                    # Detect the test name
                    # Check if the part contains the test name
                    if part.startswith("Name:"):
                        # Extract and clean the test name by removing the "Name:" prefix
                        test_name = part.replace("Name:", "").strip()

                    # Detect the range values
                    elif part.startswith("Range:"):
                        range_part = part.replace("Range:", "").strip()

                        # Check if the part contains the range information
                        # If the range contains a comma, it has both min and max values
                        if "," in range_part:
                            # Split the range values by the comma
                            range_segments = range_part.split(",")
                            for segment in range_segments:
                                # Clean each segment
                                segment = segment.strip()
                                # Check if the segment defines a minimum value
                                if segment.startswith(">"):
                                    # Remove the ">" symbol and convert the value to float
                                    min_range = float(segment.replace(">", "").strip())
                                # Check if the segment defines a maximum value
                                elif segment.startswith("<"):
                                    # Remove the "<" symbol and convert the value to float
                                    max_range = float(segment.replace("<", "").strip())
                        else:
                            # Single range, may be max or min
                            # If there is no comma, we have only one limit (min or max)
                            if range_part.startswith(">"):
                                # Handle minimum value
                                min_range = float(range_part.replace(">", "").strip())
                            elif range_part.startswith("<"):
                                # Handle maximum value
                                max_range = float(range_part.replace("<", "").strip())

                # Check if the test name is available
                if test_name:
                    # Store the normal ranges for the test in the dictionary
                    self.normal_ranges[test_name] = {
                        'min_range': min_range,
                        'max_range': max_range
                    }
    #this ffunction to check the abnormal tests result
    def is_abnormal(self, test_name, result_value):
        # Retrieve the normal range dictionary for the given test name
        normal_range = self.normal_ranges.get(test_name, None) #return the normal range for test name , else None

        #if there is normal_range
        if normal_range:
            # get the min and max range from the normal_range
            min_range = normal_range.get('min_range')
            max_range = normal_range.get('max_range')

            try:
                #convert result value to float
                result_value = float(result_value)
                #convert min and max range to float
                if min_range is not None:
                    min_range = float(min_range)
                if max_range is not None:
                    max_range = float(max_range)
            #error handle
            except ValueError:
                print(f"Error: Could not convert result or range values to float for {test_name}.")
                # Return false if conversion fails
                return False

            # Check if the result is outside the normal range return true if result is abnormal
            if min_range is not None and result_value <= min_range:
                return True
            if max_range is not None and result_value >= max_range:
                return True
        #return false if result is normal or there is no range
        return False

    #function to filter medical test as what user want
    def filter_medical_tests(self):
        # Initialize an empty list to store filtered records
        filtered_records = []
        print("\nFilter Medical Records")
        print("Enter filter criteria if you want to filter otherwise click enter:")

        # Get user input for filtering
        patient_id = input("Patient ID (7 digits): ").strip()
        #check validation for id
        if not self.validate_patient_id(patient_id):
            if patient_id  :
                print("Invalid Patient ID. It must be exactly 7 digits.")
                self.filter_medical_tests()
        test_name = input("Test Name: ").strip()
        #ask user if want to filter acording to abnormal test or not ( yes show the abnormal test )
        abnormal_tests = input("Abnormal tests only? (yes/no): ").strip().lower()
        date_from = input("Start Date (format: YYYY-MM-DD): ").strip()

        #check the validation for date from
        if not self.validate_date(date_from):
            if date_from:
                print("Invalid test date from")
                self.filter_medical_tests()

        date_to = input("End Date (format: YYYY-MM-DD): ").strip()

        #check the validation for date to
        if not self.validate_date(date_to):
            if date_to:
                print("Invalid test date to")
                self.filter_medical_tests()

        status = input("Status (Pending, Completed, Reviewed): ").strip().capitalize()
        #check the validation for status
        if not self.validate_status(status):
            if status:
                print("Invalid status. It must be 'Pending', 'Completed', or 'Reviewed'.")
                self.filter_medical_tests()

        min_turnaround_time = input("Minimum Turnaround Time (in minutes): ").strip()
        max_turnaround_time = input("Maximum Turnaround Time (in minutes): ").strip()

        # Convert date inputs to datetime objects
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None

        # Convert turnaround time inputs to integers
        min_turnaround_time = int(min_turnaround_time) if min_turnaround_time else None
        max_turnaround_time = int(max_turnaround_time) if max_turnaround_time else None

        # Load the medical tests and turnaround times from the file
        medical_tests = {}
        with open('medicalTest.txt', 'r') as file:
            for line in file:
                parts = line.split(';')
                if len(parts) >= 4:
                    #split the name from the file
                    name = parts[0].split(':')[1].strip()
                    # split Turnaround time in dd-hh-mm format from the file
                    turnaround_time = parts[3].strip()
                    # Store turnaround time in a dictionary keyed by test name
                    medical_tests[name.lower()] = self.calculate_turnaround_time(turnaround_time)

        # Load normal ranges before filtering (if abnormal test filtering is needed)
        if abnormal_tests == "yes":
            self.load_normal_ranges()

        # Start filtering the records
        for patient in self.patients.values():
            # Skip if the patient ID does not match
            if patient_id and patient.patient_id != patient_id:
                continue

            for record in patient.records:
                # Skip if the test name does not match
                if test_name and record['test_name'].lower() != test_name.lower():
                    continue

                # Skip if the test date is before the start date
                if date_from_obj and datetime.strptime(record['test_date_time'], '%Y-%m-%d %H:%M') < date_from_obj:
                    continue

                # Skip if the test date is after the end date
                if date_to_obj and datetime.strptime(record['test_date_time'], '%Y-%m-%d %H:%M') > date_to_obj:
                    continue

                # Skip if the status does not match
                if status and record['status'].lower() != status.lower():
                    continue

                # Skip if the test is normal but the user selected to filter by abnormal tests only
                if abnormal_tests == "yes" and not self.is_abnormal(record['test_name'], record['result_value']):
                    continue

                # Check the turnaround time from the medicalTest file
                test_turnaround_time = medical_tests.get(record['test_name'].lower())
                # Skip if the test doesn't have a turnaround time in the file
                if test_turnaround_time is None:
                    continue

                # Check if the turnaround time is within the specified range
                if min_turnaround_time is not None and test_turnaround_time < min_turnaround_time:
                    continue
                if max_turnaround_time is not None and test_turnaround_time > max_turnaround_time:
                    continue

                # Store the filtered record
                filtered_records.append({
                    'patient_id': patient.patient_id,
                    'test_name': record['test_name'],
                    'result_value': record['result_value'],
                    'unit': record['unit'],
                    'status': record['status'],
                    'turnaround_time': test_turnaround_time,
                    'test_date_time': record['test_date_time']
                })

        return filtered_records

    # Calculate the turnaround time for a test record in minutes
    def calculate_turnaround_time(self, time):
        days, hours, minutes = map(int, time.split("-"))
        # Convert everything to total minutes
        total_turnaround_time = (days * 24 * 60) + (hours * 60) + minutes
        return total_turnaround_time

    #function to print summary report
    def generate_summary_report(self, filtered_records):
        #if there is no record filterd
        if not filtered_records:
            print("No records to summarize")
            return

        # this total used to find the average
        total_test_values = 0

        #This is used to track the minimum test value among the filtered records
        #initialized to positive infinity (float('inf')) to ensure that any actual test value found will be smaller.
        min_test_value = float('inf')

        #This is used to track the maximum test value among the filtered records
        #Initialized to negative infinity (float('-inf')) to ensure that any actual test value found will be larger.
        max_test_value = float('-inf')

        #this used to find the average
        total_turnaround_time = 0

        # This is used to track the minimum turnaround time among the filtered records
        # initialized to positive infinity (float('inf')) to ensure that any turnaround time found will be smaller.
        min_turnaround_time = float('inf')

        # This is used to track the maximum turnaround time among the filtered records
        # Initialized to negative infinity (float('-inf')) to ensure that any actual turnaround time found will be larger
        max_turnaround_time = float('-inf')

        #this loop to iterate in filtered record and find min ,max and avg for both time and values
        for record in filtered_records:
            test_value = float(record['result_value'])
            turnaround_time = record['turnaround_time']

            # Calculate min, max, and total for test values
            min_test_value = min(min_test_value, test_value)
            max_test_value = max(max_test_value, test_value)
            total_test_values += test_value

            # Calculate min, max, and total for turnaround times
            min_turnaround_time = min(min_turnaround_time, turnaround_time)
            max_turnaround_time = max(max_turnaround_time, turnaround_time)
            total_turnaround_time += turnaround_time

        #calculate the average
        avg_test_value = total_test_values / len(filtered_records)
        avg_turnaround_time = total_turnaround_time / len(filtered_records)

        # Print summary
        print(f"_________________________________________________________________________")
        print("|                        -----Summary Report-----                       ")
        print(f"| Minimum Test Value from the filter record test: {min_test_value} ")
        print(f"| Maximum Test Value from the filter record test: {max_test_value} ")
        print(f"| Average Test Value from the filter record test: {avg_test_value:.2f} ")
        print(f"| __________________________________________________________________________")
        print(f"| Minimum Turnaround Time from the filter record test: {min_turnaround_time} minutes ")
        print(f"| Maximum Turnaround Time from the filter record test: {max_turnaround_time} minutes    ")
        print(f"| Average Turnaround Time from the filter record test: {avg_turnaround_time:.2f} minutes  ")
        print(f"|___________________________________________________________________________")


    # Export medical records to a comma-separated values (CSV) file.
    def export_records_to_csv(self,patients, filename):
        # list to hold the records , to export it to the file
        records = []

        # Iterate over each patient (that load from file) and their records
        for patient in patients.values():
            for record in patient.records:
                # put each record into a dictionary format
                    record_dict = {
                        'Patient ID': patient.patient_id,
                        'Test Name': record['test_name'],
                        'Test Date Time': record['test_date_time'],
                        'Result Value': record['result_value'],
                        'Unit': record['unit'],
                        'Status': record['status'],
                        'Results Date Time': record.get('results_date_time', '')
                    }

                    # append each record (dict) to the list records
                    # so we have list of dictonary to easy exporting to file
                    records.append(record_dict)

        #if there is no record upload from the file
        if not records:
            print("No records to export")
            return

        #determine the column headers for the CSV file based on the keys of the dictionary
        fieldnames = records[0].keys()
        try:
            #open the file in write mode
            with open(filename, mode='w', newline='') as file:
                #create an DictWriter opject (to write in csv file)
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                #write each record in separate row
                writer.writerows(records)

            #this makes to avoid print comma after status if it is not completed
            #open the file to read line by line
            with open(filename, 'r') as file:
                lines = file.readlines()

            #this list to store the data again without comma
            new_lines = []
            for line in lines:
                # Check if the line ends with 'Completed' or 'completed'
                if re.search(r',\s*(Completed|completed)$', line):
                    new_lines.append(line)
                else:
                    # Remove comma if it's followed by an empty space or line end
                    line = re.sub(r',\s*$', '\n', line)
                    new_lines.append(line)

            #open the file again to store data without the comma
            with open(filename, 'w') as file:
                file.writelines(new_lines)

            #conformed message
            print(f"Records successfully exported to {filename}.")

        #if there is an error in exporting the data
        except Exception as e:
            print(f"An error occurred while exporting records: {e}")

    # Import medical records from a CSV file into the patients dictionary.
    def import_records_from_csv(self, filename):
        #dictonary to store the records in it
        patients = {}
        #str to easy store
        str=""
        try:
            # Open the CSV file in read mode
            with open(filename, mode='r', newline='') as file:
                # Create a CSV reader object
                reader = csv.reader(file)

                # Iterate over each row in the CSV file
                for row in reader:
                    if None not in row:
                        if len(row) < 6:
                            print(f"Skipping row with insufficient columns: {row}")
                            continue
                        #split the data from file
                        patient_id = row[0].strip()
                        test_name = row[1].strip()
                        test_date_time = row[2].strip()
                        result_value = row[3].strip()
                        unit = row[4].strip()
                        status = row[5].strip()
                        #this just for completed status
                        results_date_time = row[6].strip() if len(row) > 6 else None

                        # Validate date and time formats
                        if not self.validate_datetime(test_date_time):
                            print(f"invalid test date and time format: {row}")
                            continue
                        if results_date_time and not self.validate_datetime(results_date_time):
                            print(f"invalid results date and time format: {row}")
                            continue

                        # Create a record dictionary
                        record = {
                            'test_name': test_name,
                            'test_date_time': test_date_time,
                            'result_value': result_value,
                            'unit': unit,
                            'status': status,
                            'results_date_time': results_date_time
                        }

                        # Add record to the corresponding patient
                        if patient_id not in patients:
                            patients[patient_id] = Patient(patient_id)
                        patients[patient_id].add_record(record)

                        # save the record as string
                        if status.lower() == "completed":
                            str=str+(f"{patient_id}: {test_name}, "
                                  f"{test_date_time}, {result_value}, "
                                  f"{unit}, {status}, {results_date_time}\n")
                        else :
                            str = str + (f"{patient_id}: {test_name}, "
                                         f"{test_date_time}, {result_value}, "
                                         f"{unit}, {status}\n")
            #ask user
            x=input("Please select your choice\n1. Print to terminal\n2. Print to another file\n")
            if x == '1':
                #print the records that import
                print(str)
                print(f"Records successfully imported from {filename}.")
            elif x == '2':
                #write the records that import to new file as user want
                fileN=input("Enter the file you want to print into: ")
                # Open a file in write mode
                with open(fileN, 'w') as file:
                    # Write the string to the file
                    file.write(str)
                print(f"Records successfully imported from {filename}.")

        #handle error
        except FileNotFoundError:
            print(f"{filename} not found! No records imported!")

        except Exception as e:
            print(f"An error occurred while importing records: {e}")

        return patients

    #the function that print menu to the user
    def menu(self):
        while True:
            # Display menu options
            print("\nMedical Test System Menu:")
            print("1. Add New Medical Test Definition")
            print("2. Add New Medical Test Record")
            print("3. Update Medical Test Record")
            print("4. Update medical tests in the medicalTest file")
            print("5. Filter medical tests")
            print("6. Generate textual summary reports")
            print("7. Export medical records to a comma separated file")
            print("8. Import medical records from a comma separated file")
            print("9. Exit")

            #get user input
            choice = input("Enter your choice: ")

            #add new medical test definition
            if choice == '1':
                self.add_new_medical_test_definition()
            #add new medical test record
            elif choice == '2':
                self.add_new_medical_test_record()
            # update medical test record
            elif choice == '3':
                self.update_medical_test_record()
            #update medical test definition
            elif choice == '4':
                self.update_medical_test_definition()
            #filter medical test
            elif choice == '5':
                #create object
                filter=self.filter_medical_tests()
                # Print each filtered record after calling the method
                for record in filter:
                    print(f"Patient ID: {record['patient_id']}, Test Name: {record['test_name']}, "
                          f"Result: {record['result_value']} {record['unit']}, Status: {record['status']}, "
                          f"Turnaround Time: {record['turnaround_time']} minutes, "
                          f"Test Date: {record['test_date_time']}")
            #generate summury report
            elif choice == '6':
                #call the function filter , to summary according to it
                filter1=self.filter_medical_tests()
                self.generate_summary_report(filter1)
            #export record to csv file
            elif choice == '7':
                #load records from midecalRecord.txt
                load=self.load_medical_records()

                try:
                    filename=input("Enter the file you want to export to it: ")
                    self.export_records_to_csv(load,filename)

                except FileNotFoundError:
                    print("the file does not exist")
            #import records from csv file
            elif choice == '8':
                try:
                    filename=input("Enter the file you want to import from it: ")
                    self.import_records_from_csv(filename)

                except FileNotFoundError:
                    print("the file does not exist")
            #exit the system
            elif choice == '9':
                print("Exiting the system.")
                break
            else:
                print("Invalid choice :( Please try again!")


# Main program entry point to run the menu system
if __name__ == "__main__":
    system = MedicalTestSystem()
    system.menu()
