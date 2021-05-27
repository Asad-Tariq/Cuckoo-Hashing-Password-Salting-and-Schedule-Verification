# Cuckoo-Hashing-Password-Salting-and-Schedule-Verification
Final Project for the Habib University course CS201 - Data Structures II

# Team Information
Project Team: Sibling-Variables <br />
Members: Fahad Shaikh (05452), Asad Tariq (05439), Fatima Zehra (04316), Neha Valliani (06229)

# Problem & Application 
Our project, based upon the Cuckoo Hashing data structure, consists of two modules: Password Salting and Schedule Verification.

## Module 1: Password Salting
In this module we have built a secure login system wherein the passwords are salted rather than being stored in plain text. The salt that we use is generated via a cryptographically secure function ***generate_salt*** which we then append and prepend to the password that the user inputs in the system. This is done by taking the first half of the salt and prepending it to the password while the second half of the salt is appended to the salt. Via this salt and passowrd mixture, we generate a 32 bit hash value. The username of the user is stored as the key in our hash table and a tuple consisting of the salt and the generated hash value is stored as the corresponding value.

At the time of login in the future, if the user is already registered, his/her entered password needs to be verified. This will be done in the following way:
1. The username of the user will be used to extract the corresponding tuple in the hash table.
2. The password entered by the user will be salted with the salt obtained from the hash table.
3. The hash value of ***this*** salted password will be compared against the hash value stored in the hash table at the time of registration, corresponding to this particular user.
4. If both the hash values match, the user successfully logs in.

## Module 2: Schedule Verification
The purpose of this module is to construct a schedule from a particular choice of classes, as selected by the user, from a pool of different classes. There might exist classes that are on the same day with either the exact same timings or overlapping timings. The user should not be allowed to enroll in such classes. We therefore propose an efficient solution to this problem and to implement this solution we make use of Cuckoo Hashing. We store the different classes of the schedule with their respective times as the keys and the details of the classes as the corresponding values in our Hash Table.
The very fact that our Data Structure does not allow for duplicate keys weeds out all the classes in the hash table that have exactly the same timings on the same days. Now we move on to manually remove overlapping conflicts in the user's proposed schedule to fully verify that no clashes occur.
The result of our Schedule Verifier is then displayed to the user and indicates to them that whether or not their proposed schedule had conflicts. If it did happen to have conflicts they will be identified specifically to the user.
