const mongoose=require('mongoose');
const {Schema}=mongoose;

const datosProfitSchema=new Schema({
	id:{type:String,required:true},
	encuesta:{type:Array,required:true},
	tipoEncuesta:{type:String,required:false},
	fechaInserccion:{type:Date,default:Date.now}
});

module.exports=mongoose.model('datos_profit',datosProfitSchema);
