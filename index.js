/*
 * index.js
 * Main backend file
*/

// import needed dependencies
require('ejs');
const express = require('express')
var cookieParser = require('cookie-parser')


// Establish Application
const app = express()
const port = 8080

// Parsers
app.use(cookieParser())

// Static endpoints
app.use('/static', express.static('static'))

// set the view engine to ejs
app.set('view engine', 'ejs');

app.get('/', (req, res) => {
  res.render("index")
})

app.get('/test', (req, res) => {
    console.log("test")
    res.send('Test!')
})

app.listen(port, () => {
  console.log(`Application running with the port: ${port}`)
})

