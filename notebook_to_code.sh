for file in `ls *.ipynb`; do ipython nbconvert --to python $file; done
#for file in `ls *.ipynb`; do ipython nbconvert --post serve  --to slides $file; done
