const express = require('express')

const path = require('path')

const app = express()

app.set('PORT', process.env.PORT || 3000)

app.use(express.static('publico'))

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '/Vistas/index.html'))
})

app.get('/MetodoBiseccion', (req, res) => {
  res.sendFile(path.join(__dirname, '/Vistas/Biseccion.html'))
})

app.get('/Newton-Rapson', (req, res) => {
  res.sendFile(path.join(__dirname, '/Vistas/Newton-Rapson.html'))
})

app.get('/Broyden', (req, res) => {
  res.sendFile(path.join(__dirname, '/Vistas/Broyden.html'))
})

app.get('/Jacobi', (req, res) => {
  res.sendFile(path.join(__dirname, '/Vistas/Jacobi.html'))
})

app.get('/Gauss-Seidel', (req, res) => {
  res.sendFile(path.join(__dirname, '/Vistas/Gauss-Seidel.html'))
})

app.get('/Secante', (req, res) => {
  res.sendFile(path.join(__dirname, '/Vistas/Secante.html'))
})

app.get('/Trapecio', (req, res) => {
  res.sendFile(path.join(__dirname, '/Vistas/Trapecio.html'))
})

app.get('/Trapecio', (req, res) => {
  res.sendFile(path.join(__dirname, '/Vistas/Simpson.html'))
})

app.listen(app.get('PORT'), () => console.log(`Server front in port ${app.get('PORT')}`))