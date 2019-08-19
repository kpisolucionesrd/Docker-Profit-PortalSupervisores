const mongoose=require('mongoose');
const {Schema}=mongoose;

const usuariosSupervisoresIndirectoSchema=new Schema({
	identificador:{type:Number,required:true},
	nombre:{type:String,required:true},
	apellido:{type:String,required:true},
	password:{type:String,required:true}
});

module.exports=mongoose.model('usuarios_supervisores_indirecto',usuariosSupervisoresIndirectoSchema);
