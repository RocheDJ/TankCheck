// simple scaling block all values expected as floats
function scale(fRawInput,fRawMin,fRawMax,fScaMin,fScaMax){
  let fRange_In = fRawMax - fRawMin;
  let fRange_Out = fScaMax - fScaMin;
//Added to avoid devide by zero error
  let fScal_fac =1;
  if (fRange_In >0){
     fScal_fac = fRange_Out / fRange_In;
  }
  let fOut =0;
  //actual scaling calculations
  fOut = ((fRawInput - fRawMin)/fRange_In * fRange_Out) +fScaMin;

  return fOut;
};

module.exports =scale;
