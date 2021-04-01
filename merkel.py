import sys
import hashlib
import codecs

def md5( m ):
    return bytes( hashlib.md5( m ).hexdigest(), 'utf-8' )

def hash_chain( data, n ):
    i = 0
    for j in range( 0, len( data ) - 2, 2 ):
        data[ i ] = md5( data[j] + data[j+1] )
        i += 1
    if n % 2 != 0:
        data[ n // 2 ] = data[ n-1 ]
    return data

def parse( filename ):
    ret = []
    with open( filename, 'r' ) as f:
        for path in f:
            path = path.strip()
            try:
                with open( path, 'r' ) as f2:
                    ret.append( md5( bytes( f2.read(), 'utf-8' ) ) )
            except Exception as e:
                print( "file does not exist {}".format( path ) )
                exit( 1 )
    return ret

def main( datafile=None ):
    if datafile == None:
        if len( sys.argv ) != 2:
            print( "Usage: python3 merkel.py input_file_name" )
            print("input_file_name must be a file containing target file paths separated by newline characters" )
            exit( 1 )
        
        datafile = sys.argv[1]

    data = parse( datafile ) # an array of the hashed contents of each newline separated file path
    size = len( data )
    
    # combine and chain nodes at the same depth, also including +1 node if exists
    while size > 1:
        data = hash_chain( data, size )
        size = size // 2 + ( size % 2 )
    
    # size has to be 1 now
    if size == 1:
        sys.stdout.buffer.write( data[size] )
        print( "" )
        return data[size]
    else:
        print( "ERR: no merkel tree root exists, something went wrong" )
    return None
