import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''
    Extracts data from song files. Inserts data into songs and artists
    tables.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Connection cursor to the database.
    filepath : STRING
        Path to a file to be processed.

    Returns
    -------
    None.

    '''

    df = pd.read_json(filepath, lines=True)

    song_data = df[['song_id',
                    'title',
                    'artist_id',
                    'year',
                    'duration']].values[0]
    
    song_data = song_data.tolist()
    cur.execute(song_table_insert, song_data)
    
    artist_data = df[['artist_id',
                      'artist_name',
                      'artist_location',
                      'artist_latitude',
                      'artist_longitude']].values[0]
    
    artist_data = artist_data.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''
    Extract data from log files, filters by NextSong action in the "page"
    column, converts timestamp column to datetime. Inserts data into time,
    user, and songplay tables.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Connection cursor to the database.
    filepath : STRING
        Path to a file to be processed.

    Returns
    -------
    None.

    '''

    df = pd.read_json(filepath, lines=True)

    df = df[(df['page'] == 'NextSong')]

    t = pd.to_datetime(df['ts'], unit='ms')
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    time_data = pd.concat([df['ts'],
                           t.dt.hour,
                           t.dt.day,
                           t.dt.isocalendar().week,
                           t.dt.month,
                           t.dt.year,
                           t.dt.weekday],
                            axis = 1)
    
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(data=time_data.values, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():
        
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = (row.ts,
                         row.userId,
                         row.level,
                         songid,
                         artistid,
                         row.sessionId,
                         row.location,
                         row.userAgent)
        
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''
    Gets all files in the path and passes it to the func.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Connection cursor to the database.
    conn : psycopg2.extensions.connection
        Connection object to the database.
    filepath : STRING
        Filepath to data files.
    func : FUNCTION
        Function to process individual data files.

    Returns
    -------
    None.

    '''

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()