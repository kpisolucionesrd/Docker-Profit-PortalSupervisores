var express = require('express');
const cockie=require('cookie-parser');
const session=require('express-session');
const {mongoose}=require('./ConexionDB.js');
var app = express();

//Modelos de Datos
const UsuariosSupervisoresIndirecto=require('./ModelosDatos/profit_usersSupervisoresIndirectos.js');
const UsuariosMercaderistas=require('./ModelosDatos/profit_users.js');
const DatosCapturados=require('./ModelosDatos/datos_capturados.js');


//Midllewares
app.use(cockie());
app.use(session({
  secret: 'keyboard cat',
  resave: false,
  saveUninitialized: true
}));
app.use(express.static('public'));
app.use(express.urlencoded());


//Configuraciones del servidor
app.set('views','./views');
app.set('view engine', 'pug');


//Loggin
app.get('/', function(req, res) {
    res.render('loggin');
});

//Request Inicio de Sesion
app.post('/', async(req, res)=> {

  try{
    /* Verificacion si el usuario existe */
    const idSupervisor=req.body.usuario;
    const passwordDigitado=req.body.password;

    const usuario=await UsuariosSupervisoresIndirecto.find({identificador:idSupervisor});

    if(passwordDigitado==usuario[0].password){
      req.session.nombre=usuario[0].nombre
      const mercaderistas=await UsuariosMercaderistas.find({supervisor:usuario[0].nombre},{identificador:1,nombre:1,_id:0})

      const Fecha=new Date();
      const FechaConsulta=new Date(Fecha.getFullYear(),Fecha.getMonth());
      const objetoEncuesta=await DatosCapturados.find({fechaInserccion:{$gt:FechaConsulta},tipoEncuesta:"Encuesta"}).count();
      res.render('portalSupervisores',{objetoMercaderistas:mercaderistas,cantColmados:objetoEncuesta});
    }else{
      res.send("Usuario incorrecto");
    }
  }catch(e){
    console.log("Error en el servidor\n");
    console.log(e);
    res.send("Error en el servidor");
  }
});

//Portal Supervisores
app.get('/PortalSupervisores',async(req,res)=>{
  if(req.session.nombre){
    const mercaderistas=await UsuariosMercaderistas.find({supervisor:req.session.nombre},{identificador:1,nombre:1,_id:0})
    res.render('portalSupervisores',{objetoMercaderistas:mercaderistas});
  }else{
    res.render('loggin');
  }
});

//Request Estadistica mercaderista
app.get('/PortalSupervisores/:identificador',async(req,res)=>{
  if (req.params.identificador=="Total"){
    var objetoEncuesta=await DatosCapturados.find({fechaInserccion:{$gt:FechaConsulta},tipoEncuesta:"Encuesta"}).count();
  }else{
    const mercaderista=req.params.identificador;
    const Fecha=new Date();
    const FechaConsulta=new Date(Fecha.getFullYear(),Fecha.getMonth());
    var objetoEncuesta=await DatosCapturados.find({id:mercaderista,fechaInserccion:{$gt:FechaConsulta},tipoEncuesta:"Encuesta"}).count();
  }
  if(req.session.nombre){
    const mercaderistas=await UsuariosMercaderistas.find({supervisor:req.session.nombre},{identificador:1,nombre:1,_id:0})
    res.render('portalSupervisores',{objetoMercaderistas:mercaderistas,cantColmados:objetoEncuesta});
  }else{
    res.render('loggin');
  }
});

//Corrida Servidor
app.listen(5000,function(){
    console.log("Servidor Funcionaldo...");
});