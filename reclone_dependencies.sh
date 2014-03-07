
working_dir=`pwd`
dev_dir="$HOME/dev"

cd $dev_dir

projects="GEMScienceTools/notebooks gem/oq-hazardlib gem/oq-nrmllib GEMScienceTools/hmtk GEMScienceTools/hmtk-utils GEMScienceTools/hmtk_docs GEMScienceTools/nrml_converters gem/oq-common gem/oq-engine gem/oq-eqcatalogue-tool gem/oq-platform gem/oq-risklib GEMScienceTools/oq-tools gem/qt-experiments"


for _p in $projects; do
    project=`echo $_p | awk -F/ '{ print $2 }'`
    echo "====================================="
    echo "processing $project"

    upstream="git@github.com:$_p.git"
    origin="git@github.com:preinh/$project.git"

    if [[ -d $project ]]; then
        echo "backing up..."
        time=$(date "+%Y%m%d_%H%M%S")
        mv "$project" "${project}_${time}.bak"
    fi

    git clone --depth=1 $upstream

    cd $project

    echo $project
    git remote rm origin
    git remote add upstream $upstream
    git remote add origin $origin

    cd $dev_dir

#echo $upstream $origin

done

cd $working_dir
echo "done!"
#git clone $upsgream
