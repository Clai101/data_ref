filelist=`find -name \*.hist -size +0c|sort`

for file in ${filelist}
do
    h2root ${file}  
done

