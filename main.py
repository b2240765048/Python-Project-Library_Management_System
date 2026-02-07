# I sorted ISBN numbers in output files ( available_books.txt and on_loan_books.txt ) just for better visualization.

import os

def add_books(script_dir): # Function that collects all books and their informations.
    existing_books_txt_path=os.path.join(script_dir,"existing_books.txt")
    new_books_txt_path=os.path.join(script_dir,"new_books.txt")
    with open(existing_books_txt_path,"r") as books_initial: # Collecting existing books.
        Library_Record={}
        for line in books_initial:
            each_line=line.strip().split(",")
            isbn,title,author,year=each_line
            Library_Record[isbn]={
                                  "title":title,
                                  "author":author,
                                  "year":year
                                  }
    with open(new_books_txt_path,"r") as new_books: # Collecting new books.
        for line in new_books:
            each_line_new=line.strip().split(",")
            isbn_new, title_new, author_new, year_new=each_line_new
            if isbn_new in Library_Record:
                continue
            else:
                Library_Record[isbn_new]={
                                          "title":title_new,
                                          "author":author_new,
                                          "year":year_new
                                          }

    return Library_Record


def availability_of_books(Library_Record,script_dir): # Function that collects on-loan books and students who borrowed them , available books  and books that not available.
    existing_student_borrows_txt_path=os.path.join(script_dir,"existing_student_borrows.txt")
    with open(existing_student_borrows_txt_path,"r") as on_loan:
        on_loan_books_record = {} # This dictionary will contain books that are already borrowed,with borrowers' student id.
        for line in on_loan:
            each_line=line.strip().split(",")
            student_id,isbn=each_line
            if isbn=="":
                on_loan_books_record[student_id]=None # students who haven't borrowed any book.
            else:
                isbns = set(isbn for isbn in each_line[1:] if isbn != '')
                if student_id in on_loan_books_record:
                    if on_loan_books_record[student_id] == []:
                        on_loan_books_record[student_id] = isbns # if it is the first borrow of the student, only assign.
                    else:
                        on_loan_books_record[student_id].update(isbns)  # if the student has already borrowed a book, update the borrow list.
                else:
                    on_loan_books_record[student_id] = isbns

        not_available_books_record = [] # This list will contain only ISBNs of borrowed books.
        for i in on_loan_books_record.values():
            if i is not None: # To seperate who don't borrow a book.
                for isbn in i:
                    not_available_books_record.append(isbn)

        available_books_record= [] # This list will contain only ISBNs of unborrowed books.
        for v in Library_Record.keys():
            if v not in not_available_books_record:
                available_books_record.append(v)

    return available_books_record , not_available_books_record , on_loan_books_record


def borrow_return_book(available_books_record, on_loan_books_record, not_available_books_record,script_dir): # This function will modify available books,not available books and on-loan books datas after borrowing and returning.
    borrow_and_return_data_txt_path=os.path.join(script_dir,"borrow_and_return_data.txt")
    with open(borrow_and_return_data_txt_path,"r") as borrow_return:
        for line in borrow_return:
            each_line=line.strip().split(",")
            student_id,action,isbn=each_line # action is "borrow" or "return.
            if action == "borrow": # borrowing a book
                if on_loan_books_record[student_id] == None: # A special case in which the student hasn't borrowed a book yet.
                    if isbn in available_books_record:
                        on_loan_books_record[student_id] = {isbn}
                        available_books_record.remove(isbn)
                        not_available_books_record.append(isbn)
                else:
                    if isbn in available_books_record and len(on_loan_books_record[student_id])<3: # checking if the student (who borrowed a book before) meets the requirements to borrow the book.
                        on_loan_books_record[student_id].add(isbn)
                        available_books_record.remove(isbn)
                        not_available_books_record.append(isbn)

            elif action == "return": #returning a book.
                if isbn in list(on_loan_books_record[student_id]): # checking whether the student has borrowed that book or not.
                    on_loan_books_record[student_id].discard(isbn)
                    available_books_record.append(isbn)
                    not_available_books_record.remove(isbn)

    return on_loan_books_record, available_books_record


def output(Library_Record,on_loan_books_record,available_books_record,script_dir): # function which writes the data into output files.
    library_txt_path=os.path.join(script_dir,"library.txt")
    available_books_txt_path=os.path.join(script_dir,"available_books.txt")
    on_loan_books_txt_path=os.path.join(script_dir,"on_loan_books.txt")
    with open(library_txt_path,"w")  as library_txt: # creating first output file,library.txt .
        for isbn,book_information in Library_Record.items():
            title=book_information["title"]
            author=book_information["author"]
            year=book_information["year"]
            library_txt.write("{},{},{},{}\n".format(isbn,title,author,year))

    with open(available_books_txt_path,"w") as available_books_txt:# creating second output file,available_books.txt .
        available_books_record.sort(key=int) # I ordered ISBNs for better visualization.
        for available_books_isbns in available_books_record:
            available_books_txt.write("{}\n".format(available_books_isbns))

    with open(on_loan_books_txt_path,"w") as on_loan_books_txt: # creating third output file,on_loan_books.txt .
        for student_id,isbns in on_loan_books_record.items():
            if isbns != set(): # removing users who don't borrow a book.
                isbns_sorted=sorted(isbns,key=int) # I ordered ISBNs for better visualization.
                for isbns_seperately in isbns_sorted:
                    on_loan_books_txt.write("{},{}\n".format(isbns_seperately,student_id))
            else:
                continue


def main(): # main function to call all functions at once.
    script_dir=os.path.dirname(os.path.abspath(__file__))

    library_record = add_books(script_dir)
    available_books , not_available_books , on_loan_books = availability_of_books(library_record , script_dir)

    LastVersion_on_loan_books , LastVersion_updated_available_books = borrow_return_book(available_books, on_loan_books, not_available_books , script_dir)

    output(library_record , LastVersion_on_loan_books , LastVersion_updated_available_books , script_dir)

main()
















