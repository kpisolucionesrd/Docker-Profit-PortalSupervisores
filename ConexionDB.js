const mongoose=require('mongoose');

const URI='mongodb://dbprofit1:27017/CanalIndirecto';

mongoose.connect(URI,{ useNewUrlParser: true })
	.then(db=>console.log('DB esta funcionando'))
	.catch(err=>console.error(err))

module.exports=mongoose;
