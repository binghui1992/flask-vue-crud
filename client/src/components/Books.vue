<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr><br><br>
        <!-- Add <alert> component, alert must be firstly defined in components of data() to be used in template -->
        <!-- Firstly clear the message after click Add book button, then only show message after submitting adding a
          book (whether the result succeed or not), i.e. don't show message if not submit -->
        <alert :message=message v-if=showMessage></alert>
        <!-- Add book button is used to open a new popup window for adding a book by adding "modal-open" to body-->
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="toggleAddBookModal">
          Add Book
        </button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Read?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>
                <span v-if="book.read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    @click="toggleEditBookModal(book)">
                    Update
                  </button>
                  <el-button
                    text
                    type="danger"
                    @click="handleDeleteBook(book)">
                    Delete
                  </el-button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- add new book modal -->
    <!-- This a new popup window for adding a book -->
    <div
      ref="addBookModal"
      class="modal fade"
      :class="{ show: activeAddBookModal, 'd-block': activeAddBookModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add a new book</h5>
            <!-- Close button is used to close the popup window by removing the "modal-open" from body-->
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddBookModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addBookTitle" class="form-label">Title:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addBookTitle"
                  v-model="addBookForm.title"
                  placeholder="Enter title">
              </div>
              <div class="mb-3">
                <label for="addBookAuthor" class="form-label">Author:</label>
                <input
                  type="text"
                  class="form-control"
                  id="addBookAuthor"
                  v-model="addBookForm.author"
                  placeholder="Enter author">
              </div>
              <div class="mb-3 form-check">
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="addBookRead"
                  v-model="addBookForm.read">
                <label class="form-check-label" for="addBookRead">Read?</label>
              </div>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleAddSubmit">
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleAddReset">
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeAddBookModal" class="modal-backdrop fade show"></div>

    <!-- edit book modal -->
    <div
      ref="editBookModal"
      class="modal fade"
      :class="{ show: activeEditBookModal, 'd-block': activeEditBookModal }"
      tabindex="-1"
      role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleEditBookModal">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="editBookTitle" class="form-label">Title:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editBookTitle"
                  v-model="editBookForm.title"
                  placeholder="Enter title">
              </div>
              <div class="mb-3">
                <label for="editBookAuthor" class="form-label">Author:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editBookAuthor"
                  v-model="editBookForm.author"
                  placeholder="Enter author">
              </div>
              <div class="mb-3 form-check">
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="editBookRead"
                  v-model="editBookForm.read">
                <label class="form-check-label" for="editBookRead">Read?</label>
              </div>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleEditSubmit">
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleEditCancel">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeEditBookModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
// import modules or custom defined components
import axios from 'axios';
import { ElMessageBox } from 'element-plus'

import Alert from './Alert.vue';


export default {
  data() {
    return {
      activeAddBookModal: false,
      addBookForm: {
        title: '',
        author: '',
        read: [],
      },
      books: [],
      message: '',
      showMessage: false,
      activeEditBookModal: false,
      editBookForm: {
        book_id: '',
        title: '',
        author: '',
        read: [],
      },
    };
  },
  components: {
    // defined a "alert" component so it be used as "<alert></alert>" in template section
    alert: Alert
  },
  methods: {
    addBook(payload) {
      const path = 'http://localhost:5001/books';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book added!';
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
          this.getBooks();
          this.message = error;
          this.showMessage = true;
        });
    },
    getBooks() {
      const path = 'http://localhost:5001/books';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
          if (this.books.length == 0) {
            this.message = "No books! Please add one.";
            this.showMessage = true;
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5001/books/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book updated';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getBooks();
        });
    },
    deleteBook(bookID) {
      const path = `http://localhost:5001/books/${bookID}`;
      axios.delete(path)
        .then(() => {
          this.getBooks();
          this.message = 'Book deleted';
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getBooks();
        });
    },
    handleAddReset() {
      this.initForm();
    },
    handleAddSubmit() {
      this.toggleAddBookModal();
      let read = false;
      if (this.addBookForm.read[0]) {
        read = true;
      }
      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        read, // property shorthand
      };
      this.addBook(payload);
      this.initForm();
    },
    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.author = '';
      this.addBookForm.read = [];
      this.editBookForm.book_id = '';
      this.editBookForm.title = '';
      this.editBookForm.author = '';
      this.editBookForm.read = [];
    },
    toggleAddBookModal() {
      const body = document.querySelector('body');
      this.activeAddBookModal = !this.activeAddBookModal;
      this.showMessage = false;
      if (this.activeAddBookModal) {
        body.classList.add('modal-open');  // open a popup window for adding a book
      } else {
        body.classList.remove('modal-open');  // close the adding book popup window
      }
    },
    toggleEditBookModal(book) {
      if (book) {
        this.editBookForm = book;
      }
      const body = document.querySelector('body');
      this.activeEditBookModal = !this.activeEditBookModal;
      this.showMessage = false;
      if (this.activeEditBookModal) {
        body.classList.add('modal-open');
      } else {
        body.classList.remove('modal-open');
      }
    },
    handleDeleteBook(book) {
      ElMessageBox.confirm('Confirm to delete?')
        .then(() => {
          this.deleteBook(book.book_id);
        })
        .catch(() => {
        })
    },
    handleEditSubmit() {
      this.toggleEditBookModal(null);
      let read = false;
      if (this.editBookForm.read) read = true;
      const payload = {
        title: this.editBookForm.title,
        author: this.editBookForm.author,
        read,
      };
      this.updateBook(payload, this.editBookForm.book_id);
    },
    handleEditCancel() {
      this.toggleEditBookModal(null);
      this.initForm();
      this.getBooks();  // why?
    },
  },
  created() {
    this.getBooks();
  },
};
</script>
