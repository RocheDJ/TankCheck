//from https://stackoverflow.com/questions/979256/sorting-an-array-of-objects-by-property-values

function sortArrayOfObjects(arrayToSort, key,order)
{

  function compareObjectsAsc(a, b) {
    if (a[key] < b[key])
      return -1;
    if (a[key] > b[key])
      return 1;
    return 0;
  }

  function compareObjectsDesc(a, b) {
    if (b[key] < a[key])
      return -1;
    if (b[key] > a[key])
      return 1;
    return 0;
  }

  if (order =='desc'){
    return arrayToSort.sort(compareObjectsDesc);
  }else{
    return arrayToSort.sort(compareObjectsAsc);
  }


}

//use as sortArrayOfObjects(yourArray, "distance");
module.exports= sortArrayOfObjects;