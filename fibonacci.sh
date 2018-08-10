
input=$1

x=1
y=1

echo $x
echo $y

max_n=$((input - 2))

n=0
while [ $n -lt $max_n ]
do
  xy=$((x + y))
  echo $xy
   
  x=$y
  y=$xy
  
  ((n++)) 
done 
  
   