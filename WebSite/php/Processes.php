<?php
    set_time_limit(35); #makes the program wait more before throwing time error
    function Process($F, $count, $StartIndex){ #bool function
        $info = array();
        while(true){ #keeps looping until it gets the process and its result
            $info = array_filter(explode("|",file_get_contents("../".$F)));
             if(count($info) >= $count)
                return PassedOrNot($info, $StartIndex);
            }
    } 
?>

<?php
    function PassedOrNot($info, $j){ #check if the process passed or not
        if($info[$j][0] == '$'){
            if($info[$j + 1] == '+')
                return false;
        }
        return true;
    }
?>