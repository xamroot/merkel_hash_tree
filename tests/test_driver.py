import m as merkel # symlink to the merkel.py file
import shutil
import os
import random
import pathlib

def random_text():
    return 'A' * random.randrange( 0, 20 ) + 'B' * random.randrange( 0, 20 ) + 'C' * random.randrange( 0, 20 ) +'D' * random.randrange( 0, 20 )

def make_test_files( count ):
    path_prefix = str( pathlib.Path().absolute() )
    
    with open( 'input_file', 'w' ) as f:    
        for i in range( count ):

            newfile = 'test_file{}'.format( i )
            
            with open( 'files/' + newfile, 'w' ) as f2:
                f2.write( random_text() )
            
            f.write( path_prefix + '/files/{}\n'.format( newfile ) )

def run_test():
    os.mkdir( 'files' )
    
    make_test_files( 5 )
    out1 = merkel.main( 'input_file' )
    out2 = merkel.main( 'input_file' )
    assert out1==out2, "Equivalent merkle roots for two exact same file structure inputs"
    
    shutil.rmtree( 'files' )
    os.mkdir( 'files' )
    
    make_test_files( 5 )
    out2 = merkel.main( 'input_file' )
    assert out1!=out2, "Different  merkle roots for two different file structure inputs"

    shutil.rmtree( 'files' )
    return

run_test()
