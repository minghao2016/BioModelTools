#!/usr/bin/env/python
def openness_gt(df, closed):
    '''Calculate the percentage of opening in certain run.'''
    return (df[df > closed].count() / df.count())*100

def openness_lt(df, closed):
    return (df[df <= closed].count() / df.count())*100

def openness_gt_lt(df, closed, opened):
    return (df[(df >= closed) & (df <= opened)].count() / df.count())*100


def domain_opening_statistics(df,crystal_distance_closed, crystal_distance_opened=None):
    '''Calculate statistics of domain opening
    
    If only ``crystal_distance_closed`` is supplied, calculates the % of frames
    which are > than ``crystal_distance_closed``.
    If both crystal_distance_closed and crystal_distance_opened are supplied
    calculates all intervals
    
    Args:
        df (pandas.DataFrame) : rows are frames, columns are runs
        crystal_distance_closed (int) : distance of closed crystal
        crystal_distance_opened (int) : distance of opened crystal
    
    Returns:
        pandas.DataFrame instance with mean, std and percentages
    
    Usage:
        #rluc8_distances is dataframe created earlier
        >>> rluc8_statistics = domain_opening_statistics(rluc8_distances, 12.9, 17.1)
        >>> print(rluc8_statistics)
                                     run1  run2  run3  run4
        mean [A]                     17.3  13.6  14.4  13.5
        std                           1.9   1.2   1.4   1.2
        crystal distance opened [A]  17.6  17.6  17.6  17.6
        crystal distance closed [A]  12.9  12.9  12.9  12.9
        % =< 12.9                     1.2  27.5   8.4  32.0
        % =< 12.9 =< 17.6            55.5  72.2  88.6  67.9
        % >= 17.6                    43.3   0.3   3.0   0.1

    '''
    df_stats = df.describe()
    if crystal_distance_opened:
        df_stats.ix[r'crystal distance opened [A]',:] = crystal_distance_opened
        df_stats.ix[r'crystal distance closed [A]',:] = crystal_distance_closed
        df_stats.ix['% =< {}'.format(crystal_distance_closed),:] = df.apply(
            lambda x: openness_lt(x, crystal_distance_closed)
        )
        df_stats.ix['% =< {} =< {}'.format(
                crystal_distance_closed, 
                crystal_distance_opened),:] = df.apply(
            lambda x: openness_gt_lt(
                x,
                crystal_distance_closed,
                crystal_distance_opened)
        )
        
        df_stats.ix['% >= {}'.format(crystal_distance_opened),:] = df.apply(
            lambda x: openness_gt(
                x,
                crystal_distance_opened))
    else:
        df_stats.ix[r'crystal distance [A]',:] = crystal_distance_closed
        df_stats.ix['% >= {}'.format(crystal_distance_closed),:] = df.apply(
            lambda x: openness_gt(
                x,
                crystal_distance_closed))
    
    df_stats = df_stats.applymap(lambda x: '{0:.1f}'.format(x))
    df_stats.drop(['count','min',
 '25%',
 '50%',
 '75%',
 'max',],axis='rows',inplace=True)
    df_stats.rename(index={'std':r'std',
                          'mean': r'mean [A]'},inplace=True)
    
    return df_stats
