int i,c=50,a=0,b=0;
foreach(var s in File.ReadLines("i")){
 for (i=0;i++<int.Parse(s[1..]);c=(c+(s[0]<'R'?-1:1))%100)
  if(c==0)b++;
 if(c==0)a++;
}
throw new((a,b)+"");