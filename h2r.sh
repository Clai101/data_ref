if test $1
then
    dname=$1
else
    echo dname number is missing
    exit 1
fi


filelist=`find ~/Documents/data_ref/${dname}/. -name \*.hist -size +0c|sort`

for file in ${filelist}
do
    echo "${file}"
    h2root $file
done

hadd all.root *.root 
