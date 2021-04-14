from django.shortcuts import render, redirect
import requests
from .models import BS_tab

# Limit the maximum number of items to strore in the bookshelf (Databsae)
maxnum_items_bookshelf = 10 

# Read and fetch data using Google Books API
def api_fetchdata(subject):
    global matrix_data
    matrix_data=[]
    rownum=0
    rq = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + subject)     # gives the respons type <Response [200]>
    response = rq.json()                                                              # extracts the json data
    try:
        all_items = response['items']     # extracts value of the key "items" which is a dictionnary by itself
    
        for item_num in range(len(all_items)):
            rownum += 1
            # Extract data from dictionary (json response)
            itemid = all_items[item_num]['id']
            title = all_items[item_num]['volumeInfo']['title']

            try:
                cover = all_items[item_num]['volumeInfo']['imageLinks']['thumbnail']
            except:
                cover = "/static/img/book_cover_backup.png"

            try:
                subtitle = all_items[item_num]['volumeInfo']['subtitle']
            except:
                subtitle = ''

            try:
                pre_authors = all_items[item_num]['volumeInfo']['authors']
                authors = pre_authors[0] 
                if len(pre_authors) > 1:
                    for author_num in range(len(pre_authors) - 1):
                        authors = authors + ', ' + pre_authors[author_num + 1]
            except:
                authors = ""

            try:
                publishedDate = all_items[item_num]['volumeInfo']['publishedDate'][:10]
            except:
                publishedDate = ""

            if all_items[item_num]['saleInfo']['saleability'] == 'FOR_SALE':
                price = str(all_items[item_num]['saleInfo']['retailPrice']['amount'])
            else:
                price = all_items[item_num]['saleInfo']['saleability']

            previewlink = "https://books.google.com/books?id=" + itemid

            book_data = [cover,title,subtitle,authors,publishedDate,price,previewlink,rownum]
            matrix_data.append(book_data)
    except:
        print("There is no book registered in the database of Google Books with the name '" + subject + "'")
 
# Count the number of stored books in the Database
def rowcountfun():
    row_count = BS_tab.objects.count()
    return row_count

# Create your views here.
def bookshelf_app(request):
    #read data from database        
    bookshelf_db = BS_tab.objects.all() 
    try:
        rs = request.GET['searched_keywords']   
        research=rs.replace(' ', '+')       # In case the user runs a search with two words or more 
        api_fetchdata(research)
        if matrix_data == []:                # In case the application doesn't find any book with the searched name
            return render(request,"bookshelf_app.html", {'search_status' : "not found", 'searched_book_name' : rs, 'bookshelf_objects' : bookshelf_db})
        else:                                # In case everything works fine 
            return render(request,"bookshelf_app.html", {'search_status' : "found", 'reasearch_tab' : matrix_data, 'bookshelf_objects' : bookshelf_db})
    except:                                 # Bookshelf home page
        return render(request, 'bookshelf_app.html',{'bookshelf_objects' : bookshelf_db})


def add_book(request):
    book_to_add_id = request.POST['book_to_add_id']         # Identify the id of the book to be added

    # Copy data from the chosen book 
    for datarow in matrix_data:
        if datarow[7] == int(book_to_add_id):
            chosen_book_data = datarow[0:7]

    # Count the number of stored books
    row_count = rowcountfun()

    # Add the chosen book to the database if there is an empty space, otherwise display error message
    if row_count < maxnum_items_bookshelf:           
        BS_tab.objects.create(id = row_count+1, cover = chosen_book_data[0],title= chosen_book_data[1],
                              subtitle = chosen_book_data[2], authors= chosen_book_data[3],
                              publishedDate= chosen_book_data[4], price= chosen_book_data[5],
                              previewlink= chosen_book_data[6])
    else:                                   # in case the Database is totally full
        print("db is full, you have consumed your free 10 books saving ;)")

    return redirect('bs-homepage')

def delete_book(request):
    book_to_delete_id = int(request.POST['book_to_delete_id'])

    # Count the number of stored books
    row_count = rowcountfun()

    # Django instructions to delete the chosen book data from the database
    BS_tab.objects.filter(id=book_to_delete_id).delete()

    # SQL instructions to update the id of books in the database after delteing a data row
    # mycursor = mydb.cursor()    
    for id_to_upd in range(book_to_delete_id, row_count):
        BS_tab.objects.filter(id = id_to_upd+1).update(id = id_to_upd )

    return redirect('bs-homepage')