const mongoose=require('mongoose');
const {Schema}=mongoose;

const usuariosProfitSchema=new Schema({
	identificador:{type:Number,required:true},
	nombre:{type:String,required:true},
	apellido:{type:String,required:true},
	password:{type:String,required:true},
	zona:{type:String,required:true},
	supervisor:{type:String,required:true},
	es_supervisor:{type:String,required:true},
	cantCampos:{type:Number,required:false},//Cantidad de campos que debe tener el json final
	cantCamposForm:{type:Number,required:false}, //Cantidad de campos que debe tener el json final para formulario precios
	estadoColmado:{type:Array,required:false}, //Campos para la seccion Estado Colmados
	dispColmaderoSiNo:{type:Array,required:false}, //Campos para la disposicion de los colmaderos Si No
	dispColmadero:{type:Array,required:false}, //Campos para la disposicion del colmadero
	tipoAccesoColmado:{type:Array,required:false}, //Campos para los tipos de acceso de los colmados
	tamanoColmado:{type:Array,required:false}, //Campos para los tamanos de los colmados
	capacidadColmadoSiNo:{type:Array,required:false}, //Campos para la capacidades de los colmados
	tipoVentana:{type:Array,required:false}, //Campos para los tipo Ventana
	iniciativasVisibilidad:{type:Array,required:false}, //Campos de iniciativas Visibilidad
	surtidoColmado:{type:Array,required:false}, //Campos Surtidos Colmados
	actividadCompetitiva:{type:Array,required:false}, //Campos Actividad competitiva
	cuidadoOral:{type:Array,required:false}, //Campos para el formulario de precios Cuidado Oral
	cuidadoPersonal:{type:Array,required:false}, //Campos para el formulario de precio Cuidado Personal
	cuidadoHogar:{type:Array,required:false} //Campos para el formulario de precios Cuidado Hogar
});

module.exports=mongoose.model('usuarios_profit',usuariosProfitSchema);
