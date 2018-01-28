# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 11:03:20 2018

@author: thautwarm
"""

from tkinter import Scrollbar,Tk, END, Button, Text, filedialog, N, S, E, W
import os
from collections import defaultdict
import pandas as pd
import os
import time
import base64
from linq.standard.general import GroupBy, Map, Filter
import math

# Icon
img = b'AAABAAUAEBAAAAAAIACaAgAAVgAAABgYAAAAACAALAQAAPACAAAgIAAAAAAgAIsFAAAcBwAAMDAAAAAAIABqBwAApwwAAEBAAAAAACAAwQkAABEUAACJUE5HDQoaCgAAAA1JSERSAAAAEAAAABAIBgAAAB/z/2EAAAJhSURBVHicrZPPS1RRFMe/5/549828NzON5IiSlRYIBSpatAmmyFy5aOW+XQi1img3TrSKlq5DCAKRQioIpdIW/QPZxoKBKKmwYmZ0dGbeu/e0ECdNqBZ9VwfOOR8Oh++XsFsMKqBAS5NLAueA3FqOZ8dnLf4galUFCBThfh/IL+ZVX6qPRoZH9vTGadzuBQDIT+VDfSDZ4xyfFI4HWGAIlg++uLxwGtgPbwHyU/lQBf4MFA1KFp0qoYgJcNaCm4zB7v45rUwkiNhoQ9bZstuKrhXPF+sKABrGeIpoVChS1WqVo1psjfbYFz552hOHO45cMtqgHtVRRwOb5RrDpG8C2AaoSLNTUUU7nR09fpHaklm58u0d3nxdRiACDIT9NqkT3J5s54elR2SdrSRckwFAAEAmA1hnZeiF4sbZ6+hMdeL2hSJOdQ2j0qhg/sOCfLAyo1bXVxUA5cBy5wfi95eU62U8ez8PgNAR5GCdBYPRmzmK7tQhHMv07tkQuwvHFkZ6uHpmAk9WnuJ56SUCL0DaS2MrrqMWb6JpIzA7ABkAgNoBOABSKGipMbl4C5/XvyBlUvCkxsTAFSx/X8a9t9PwjQ9PeqjElV8XVCqAFNJuNDfcndd32TqLbCK7TWYAzFYLHWuhY094MTO33KkAINYRGRKZmGKxWHrFvvatIMFgUMM1xXTpvqy5GoJ0AK014nLcZqRHLYBpNJrQ/gJb6g/9sEsYIUkQHDOowfi49mku9ILIwbGVlkAoo17d3GflscdjydqPqEcJOuHYDZIQQxy73F+tDOD/hAkMKkwWaAn/HuefnvgHdHynJdMAAAAASUVORK5CYIKJUE5HDQoaCgAAAA1JSERSAAAAGAAAABgIBgAAAOB3PfgAAAPzSURBVHicvZXLb1VVFMZ/a+1zzj23F8rlUSqJWlp5CLVIJDEhMWmRR00cODCXaByoIf4JjBtMlIkGB8ahJIoDaZj4TDSxITjBgZjwUIugjCiUUi/0tve89nJwK0JbaWPUL9mTfc7e3/rW/vIt+I8hi34fQmq9Nbl+/rqs7V1rw/uHi39ONzSkteM11z/SH9SO19zf/VY7XovMTBZa2L1F31/BEPp097PrzKebRbVPhL6wLdyeTqXHvnn1q3eWUnNw92W7up/pFi22Usg2cfo4xlYsX+/isOJCxeeGxo5wOhw5fOrwyvHyuItmOgqA0rKmxS6WG1eD9O3Bg42/FBiCYP1HnqsGK2dGg0rUIQaG4XPDco/33gviBSEtUt3QuSHZ1LmxmWapiKqBx5uZBk6KrBizJHvy0K5DU2YmdxQUpVwCIcxnsgKPV1RFRAQVFVFvpggIQmZZueEb5dSniAkqSuxiVAWPRfVSezS/RS1BXkScN6/1tC7ePIYRaEglbCPQgNSnbFn5qO3t2k1W5KgIU2mD02OnLc9zQSQp5aktTGCImVFyJV7YsZ/l0XKcOi5OXOTklVMUvkBavhBBMIwoiBno3MGZ8TPkfkbmGmeOAvDmiYKI13YcoN6sc3VqjFrv8+z8dSdDI4eIXMSFiR9pSIOZbIZqXKVr+UOo6IIuWnC3sAxvnuHzJxg4uptTV75lV3c/HW1rSIuU2JVoj9qphBVUFEFoZA28+aURQOvQA8s6GVg/wCOreqg36zSyBk4cCKQ+Y1W8ij0P7yYOYvZ17WV1eTWFFay4X4sAnDims2kGN+5j74Y93JyZ5PWTb9DIpgk1JPM5hmeieRNFKAdlAH5P6jhx1BcjKCwnCiI+H/2S978/SuZzbie3qUQVppIp1pY7eGnzi3xy6VOGL57gp8lRfr45ShSGS2uRAKGGJHnCb5NXKKygLWwDIPMZfWseo2dFN6/0vkxXexcXJi5QctHsQ9s9d81ToKJkPueDH45x9vo5quUqWMtdTubmn8GsrW02EubiXgLBRIQ0z3j3u/couRJxGN9xh5kRacTZG+fsUv0yn136gmvT1ygHZbx5MzPmSpijwNSMQkR8tVRVw8R730oMWvnk1DHevCEf/zJMlmdU4gpmhpqKCxx54kuJi2QegUsCo5JlQTlwYuIMw3KDHKwlwc/WpmKSqNemeKSwfLZiMfMmIGPtya307vdsYQjtf3BfTxjI5gLrE5HtImzB6NFQl2nksMII2gKKyfytgZ6n3lworgMfpAe33x3Xi2Dww8F1iS82BaZ9hmwLK+ETya3ko5EDXx9Z7Ox8/O8jszWQqA3X9N8Z+kvHoq39E38A8TL0UBVPy7QAAAAASUVORK5CYIKJUE5HDQoaCgAAAA1JSERSAAAAIAAAACAIBgAAAHN6evQAAAVSSURBVHic3Zffb1zFFcc/Z2bu3Xt3vTGrRCGGtrSKSWJHalwcED+CoA9pHmohVGEkVERb8VhVBQn1paoS/w19qKjal7ZWVQIICSEUaKo4T6SNm0YiKUoMApofyIb8WHu93r135vRh1yb2rtcpTVupR7ovc2fu+dzvOXPmDPyfmPz3Fipy8NBBOcYxA7B191Y9/ORh/58BUGT88LiZPTMrAFOHpjyCrp02+uJoNH1pzDMxEf5tgPGXxu3smVmZmpjKuy148FePlZNi82vkDEsI3xAxu1V1W3lTemBPZc/1y+XLMjA/0AEJcHbubIdaPRV4ZHJsi/HNHeJ1SET2IrITZQhhq0ucQQSxkFWz+tEfHCn+K3/eFWD0xdGoP97yrDE8oLATZYdYqdiCA0CDEvKA5gFV9YKoGhWjpj5y154flYvlWvBBDGaVAmJEo0IkzXo2e/DBnx6Hz8PYAlAEQfdN7qsUstKVaFNMWPIEH1CvCngAVRVBTHuVtMeIXczDX3+Y2EWorlZf23Nc5KhdXVgMkg1M3D9RVVUREXU3TrZNqwqf5bWsX3MFsAgCOACR7hFTVWrVBZ+5WMMaACsGVVXrrCjaoI658f0qgJYTbHtcEcSK7XSIEnR1wqcusZGLVxRYFqnhG8tCiCCyNjs7ANY6qjaqKPr5h0WIbUziElQVr57EFXjunh/TF5fQdjyDBqpZlV+e/jW1rIaT7q66jgqCV08xSvnJQy+QugRnHU3f5OPr/2Dqw+Oc+/Q8aZQiImQ+4/UP3iBxBQAavsH227az9/Z70M6ycXMKKIozEQcG9wMw35ynHJcBeHL3Ezz/5gu8O3eGxCbkGjg1ewpnIwShli0AcO/toxsCmF4vVZWFrMZitsj3Xn2WscnHOXlxmsQlPLZrjMxniLSytBgVKbWfvriPxCUtB2LaefwFAACsWBCh4Zc49+k5Tl6axqunklawxq7kRtCw8tSyRZbyJQBqWY0sZOtC9EzCtg5YsXyl/y62V7ZzYPBbWLG8N/cePviVrbnsILYxT+96ioG+Abx6nhn6LuevznBi7iSmC0RPABHwIZDGKb8Y+/nK+DsXTvCHd1+mFJXw6rFi8doqXHnIOX9thpGtI1gx9MVlznz293WDsME2bMUwCzm/Pf075hvzXKheZPrSX1vVzThUlUwzynGZoc27OPnJNKdm/0YWMu7bdi8vn3uVel4nLaT40Hlq9w6BtnZDI28wefr3XG9UKdgCaZQgIq36gOLE8Z3Bx7m7Mkg5KvPHj48yc+19Zq69jyDEJu4o0TcFIAilqHXI9Sf9CII1LbmXC45XT9GlfKnvTlSVb375EWIb89ZHbxOZ1tmwtmreFIAgZCHj7Q+OAtDIGwQCojfXRKnqikK9rCuAohgxLPklfnb0EACluIgR0/FBI4ZFX+fiwkUGK4Mcu3CcIx++RerSdWXfEGDZBKG/sAkAr50JtBKG4Hll5jWGNw/x58t/IXXpho7XBVDFC+RtD9bje2quKLHEzDer/p1PTmhik26yKyBKpySrAHzsxWVsdqXoxoYE2kDtJkJonbYrYCpKsdxnC1FMCKHD/Q0NSaIpqzKyBdDudOsL9YVC1PfDZrV5n8DdwA4xssUmzi3LE7LQAgutlgyDeO/rV69c6dmSaSFIQOcm7p+YB5B2a9BT3n2T366kvrkjBNmpQfaKZRdBh1XYFqWRFRGw0JzPFv/0/SOlXt9az3q15R46g7n/N/tLeTBfFcKQYEZUdEQCA2kcHxi9Y/TaLW3L115MHuXRMNHl8jF8cDg+y3h+Sy4mG9otvprdKvvCl9P/uf0TeBybY+PJDY0AAAAASUVORK5CYIKJUE5HDQoaCgAAAA1JSERSAAAAMAAAADAIBgAAAFcC+YcAAAcxSURBVHic7ZldaFxpGcd/z3veM+dMmjHbbdJ23Urd2Dbdph/BFRXXdtqlKyuLxZtZ8UJxBakU9U4EQaa5EUQQlGWhoisI3qSI68dF01a2abbrB9RV0NKr2o+sYLZpm85kcjJzzvt4MR9Nmpl0ZpLiLvQ/DMyc8378n+f5P+95zvvCIzzC+wbyfhlUUMgfz8s5zhkOwsTBiaR69b0HQZG85k32jazNjeW8Vg135XMpdO0d1smAgkLuZM5MD0zLxnc36smXTibNGmbHsr2mFAx5Kruc6HYxDKuTrSlPnjv1pVN3UWStImJb3sljcsM5mR6YlolzBx2jow6Bk9wjnRvLebOzs31l9GljzYgRhhQdZk6GEfpN4HnWNwCU58oLmeADUotCB/QVRGo/lqPtCDxz4hl/g79hc2x0NypDRmSPwj6FbQJ9Nm0RT3AVh4sd6hRVdaKSYDCqWphdmHny4tGLpXbnbAetDJBDJw4NmlQ4oprsFo8hYC9OBsVK2gs8kCpZvUc2EUQVFUFMbWRBUfFEnHOF7RueenrzwOZCZCMJ4/CBMeiJe7S0MZTj279VEJE2IlDT5pHXj2SKt6MrNrT9xhpUtUo2UdSpAkm1uRpRkQbZFlBVrLH6iW0fL/rGV9X29KOo+oEvlaj81hPBpiNHP3Y05j4pNc2BcqEsgoSu7DSJklhRgyA1slLvJ0j7IhTE87yM8aoOadOCalcxz125faUHmL1/AWiZxCokNd9aEXmAj9uDS5w6dW0bIIg6nCCUwkxzybVehVQ7cG97cOrE4dAVliAjZhEFRUQExbSi0tqAFpAWI61Eqo7QhljPNo1AVRdKOSl3xKdjA2KNm04uInjioegSgoKQkBB4Ad8YOUaPn0ZrQl4Mp45yUubVf5xgPp5fEok1M0AQMqlelkpLa5NXKJQLpEyKwAY4dR2NHHhB26QXoy0DBCHWmN5UL699/mcNL6oqTpWFOOLW/G3+Of0vfn3pN9yYvUHaT+O0qneDYSFZ4JW/v7pMQk4doQ355six6pgdVhhdRSCwwdIbQYaBdQMM9e/gwIf38+3x73Dl9r8JbLCEbBRHWF1uwOLxO0XHMYs1RlGiOOInf36FH174Eb+7/AcqLiZ2MQM9/Xz1oy83SC4mZcS0/HaLjpO4TirWmN9e/j2FcoGKi7kV3eIrI19GVdm3aQ/r0+spLBSwpqsp2kbXpgtCX9jH4z2P0xf08bf/vF29LkLaT5MJenG4FR8liSY4dUtkVP+faNNKfRlW5Z658hzFSpHiQpGtj20Fqg+fKI4olksYTIsiuIqMn6HsyoQ2bFyr/06ZFKXKgwvXrg3wxGPkiX3MV+YZ6t/BF/d8gdjFWGP5y9RfmSndpMfvabqcCkLsYvZt3MuhLVlil2CND8CxvV/HGo83piaYnHqTFKm1NaCelIEN+MHz3192/9qda/z04s+xxjZdEutPXM94nJ+aJPRC9j/5bCPpQxsw+c4Fzk9N4ov/QD6rkpBqdd2OXUyxPMeF6xf4xdu/5Gbp5rIltI6Kq9TLa3zjc+rqOM4lZD90AICJG+c5ff0sgResKL+uDah7NYojvnv2e8zH88RJwvTcNDPzM/jGJ7ThUunUEjmKF/jcthdRVU5dHSe0IaENOX39LNarertBvk10HQGnjkvvXqawcBff+BhjWOevQ2ulxf1IXMJnth7m0x/8VK1/wulrZwltSOAFjF89A9AR+a4M0EWftA2IXbpaxGlz4oKQaEImlWH/lmcbJUh2ywFAGL96mtCG+LXnRaelRMfPASsWQbBicTXS9Vx4ECqu0qhcq0bs58XBz5K4pCvy0GEEFKVYLuLUUaqUuppwOaQxdjdoywBF8cQjqkS8/PrXGkthVIka7wDtwDd+Q0JGDBNTkw0JdYuOJFSPQKFcoFgutkVcqZItxSXefOctBMGI4fzUJGdqSbwadJzEVu516STsnng1bwc4Vcavnel4xWnKp9MOXWm11iW0IaevncWprgl5WMmAFjthq4KinudhVEFp+m68hAJS9ZfQ8v10hW0V6tkZA9LuLtxKMNZIhxtbYqzBLbieqBg1nbOpAalMSit3osikvF5jja9KdcN2+T6oEdo0StEkSYpGTdtbiwjOYIyK/Glw/WCJei24pEmLrodfO7zNqd0nnu5UdIfAMCo7xEivl/YQEVy8aCfaPbzNXX51qzg6OtpURm1LITeW82bimX63kNrtwS4R3akworAT9DEbWmOswcWKxg6XOFB1POTt9bYOOA6eO+hGXxpNgP/Wvn+sNzs8drgvKZlt8XxlRMTsVtiJ6m4xssn41vdSxgCUi+X04PpB/6JerB5wtFUsw5odcNDBEdMnx3Lp4O6djxhr9qBuyBizV5WnUp5k1/qIabWoHvLl8yabz9psPmtp4ZQXfvxC8P8+5GsfiuSP5+XS8KXqGdt7+Ji1EzwcZz3CI6wO/wNOdqsyjJjeoAAAAABJRU5ErkJggolQTkcNChoKAAAADUlIRFIAAABAAAAAQAgGAAAAqmlx3gAACYhJREFUeJztm/tvHNUVxz/n3pkde+P4wSOExMHGITEhDSVGiJYGmaQRpK2qUlqXn/tDS1Wpv/ShUiplcf8DVFqJFrVIrQSKk1BV/NCQQBKgEiqlDyDUsXmFhrxDHvbuemdn7ukPs948WK/X3nUSVH9Xo92duTv3nu89r3vnLMxjHvOYxzz+fyGXq99MJiNvr35bju07JvdwjxscHHSXaSyXBEImYwa2DNj+3f0eUxB/+xO3+1Ndm7uBNRKKDAwNmGP7jsmi1Yt0aGDIIWilpnf/7t5lVnWJNdKpIr0G+hwst8fdup0/2Zlt6LiqwKvr14pkyMieR/cYgL2yNxpiKD6/SX+m3ws6g9aw2a6SKL5VkLUicpOqdgFL/QV+oCqgiuajKGgNJgkTqExeI1ELAUImIwOV7FXQQQYVcAD9j/e30JTq9qx0YrQHlT5V+iJkpY1cs/GsMb4BwBUdLnYUs1FU0hKrSmFuxKwm3HRQpJIab3psU1Bsly51UZ+IWaW41YLcqEi3F9irjG9wkaKxQ2NFVcGhik6SJ6IiSDLTYkScc7mr021LOno6cqfeOyUdPR11aMDtnHpvlxv61oUaeTFq8gEbn9y4JDamGyNdwGoRXYPKWoHFYsQ3vkGsoLFOzqwTxCkqIiKlfqr1lRAQa/bFb+9oqV3I+jHVoATQTY9tCsJWt12MWYnTbr/F91Q1ETRyqFNQUDQRWMsCm9mMRJT4c8s//1zK+pFTV1HzaoWxhjiOtwzetXlLaVwV71XVB8Rh7BnPftl4hjiMKY4XIwQUNeepL4IYwCSyzw6qirXWLmhf8DXPeCj1pQXGs2RPjn0xszvzZxGZYAqnWpWAoDXQXByOqeoCFJCkvSBzE60VcmfzkW8sWl8AUGOMqBCwsLo21hIFrCBG0TkPSQBSb2hOoIAIUphu0DO31U8TdHo9bQTbDYWq4lRrMgEB6vE7cAUSkLIpvBn4gKIr1tVf3QRYsZUdok6+lV7TuBBVxTc+P1j7fZq8oGpbQRARiq7IY/94nEIcYmapCXURoCinJ05XvihgMBhjSVmflEnh1E07s21Ba839G6nfhc2aAEXxxHLfinsTLbgIsYsJ45CxwhiHxg5zePwwaT+NNXZKbXDq+PexN0h5qYrXBSFyETe03kBraiGxVs1ya8LsCVAl5aX4xfpM1XaFqMChscP8/fDrPP3GM5zInSTwgk+QICLEGvPH4afxpLIPMGIYC8d46LPf4TNXr57WrGpB3SaQDXMEJZsVwBp7wfXAC7ixo5sbO7rpW3wbj7ywmaPjR/GNX1HIFr9lSidoxCCAJ43z3XUbkTUWr3SICCMnR9l/YoQj40eYzJ2cOiIXsfyq5Xzvju/i1E0Zvpy6qkdcgx+ZCRoaBsO4yI93/JR8MY+IcNNVPfzoCz9keUcPqkkkuHPpHfRe08vw8WGa/WacXt6twIZngrFGRBqhqrx26HV++eqvCKMQIwanjrSfZllbJ6ErTq6lLisaToBMvkRYmFrIobHDHMsdR0RwJOrb0dSOFVOzKguCEVM+zifugvOzyAUangmePyCnDiOm7CQhEaYQh6i6mjRASBKe0IVYsYwXx4k0AkpOuJijEBcwkpAU2OpJ1MVoOAH5Yp5cMY8VQy7K8WD3ANemr8Gpw4oldjEHzx5EakxiYo1ZvOA6rl9wPZGLKMQF2oN2IMlCb1t0K2FcxDOWfJTnvTMfzMiwGkqAEcO6rnVMRAXaglbWLrmN9d39KIpTh2c8/nnkX7x1dB9pP12zA3TqWLf0Lq5tvvaC877xeeCm+8vft40+m/RTITGbCg0lIGV9Nvf/HDi3Sku8P3jG4/TEGX792hOEUUiT31SVgGQ/TLFiOZI7ypNv/p4He79JT1tP2bRUFQRyxRxbRray/9QIaT+NqtbsYBvvBEUucEYiginlBw/v/BnDx4drEv58Ow9sQD7KMzSynQNnD2DEEGuMiDARTbB19FneOf0uLX7LjJ8kNFQDVJX3T79fXs8X4yInsid49aO/sfv9PYyH2emFL63yOpo6GAvHkqQJIWVSZKMsz+wf4sHeAbpbu5iIJhga2cbIqRGavOr3nQoNToRCHt75CLniBEYSb39m4gxGLM1eE83TDtJQiCa45ZpVfLXnK7x54i12fLCLlE3SZt/4ZItZto5u50vd9/HG8TcZ/nj/jPzJxWisBgDjYZZcMV+Oy21BW9kJTqv2rkhvx0q+seIB0l4zdy9dh1Nl14cv4FsfNHF84+E4QyPbUJRmr75ssuFh0IrFGpus1ZWal6yqjsAL+PqK+0mXhBKE/s67ARISjF/uQ8uPrOpbFzScgMndn5kOTEnCaLPXDJzb7FC0TMLOAy+UzWHyWr2om4DYxUQuLn+u+34aA/4F51QTEqwYdn34YkN2giZRFwGCsCCVPnezVHpOFzi1Zo8zwawJEBHCOGTz7sHyllisyTZYPVvVlWZXRNh78GV2HkgiQiMxewIQIo3ZMfr8BedbgpZZa4FTRyEuENhU2QmKCC999ErJ/ivvFdaDunRKENqb2mlvLh1N7bMW3oihEIc8O/onctG5MPrSwVfYVXJ+c2FedRtVrDGxKx117NIqimd8/vPxMNtGt3M2PMvLH/2V5w/sxDNeQ0JeJVxhT4YcTV4z75x6l6f2/YEzhTP4pZmfC+HhCnw4OvmE6ET+JIpiqH3naDa44ggASnm/V/48a9RQYVKLCcTlwqZLUMSoECXv9RVIAKJOp53gqgQUzhZEFtuFtlQigyMpkVEV4aLdyUZAIN3a7NVdIqNgfEv24/FxHat+o6oE2JSN4lj/4jRegXKD3+L7qpwrfYvLef95RVIIlCvDaoaI4GIXZ09nG1IkZX2Lc27r4PrBiWpFUjUNcsNTG5aq87qsSqfz9GZRWaWqfQhdIhJY3yKeQZ3iijEaqZKYTq2EXHFlche3+QR7t2QGUp03n7nOFWQtomvUsVqFbpRu49vrvSZ7rpxuslBSUVV1IqKqaoRPR6FkzaXt/bv7veC/QXes0q0iXaJujSh9iqxRdKGxxhrfIiYpldVIUdVzpbKOfDr0Fz330HM5LlGtcH1OTJHMoxnZwx7DPbB3/d6oUpuNv9nY6lpMr0S6SlX6RLkZ6FJhmZ9OpRHAKcV8FKULftunh4CLcR4h05XLb/jthus83+uMDMvEySqEO9TpSntC7yyVy18SAi4VhAzlP0xkMpmK8fmWLQMpLt+/WC4xJgnJ9HsZrUzIPOYxj3nMYx5zi/8BETLIfwV2UvoAAAAASUVORK5CYII='
with open("./tmp.ico","wb") as tmp:
    tmp.write(base64.b64decode(img))

    

# Constants
indent = "      "
BEGIN = "1.0"  # Tkinter beginning marker.
CHINESEFONT = 'FangSong'
BOM = "\ufeff"
CodecList = ('utf8', 'gbk')

def parse(text: str):
    """naive parser for the script we use here.
    """
    cell_head = None
    cell = defaultdict(list)
    for line in text.splitlines():
        line: str
        if line.startswith(BOM):
            line = line.strip(BOM)
        if not line:
            continue
        if line.startswith(' ') or line.startswith('\r\t') or line.startswith('\t'):
            cell[cell_head].append(line.strip())
        else:
            cell_head = line.strip()
    return cell
    
        
            


def call_open_filenames(manager):
    def callback():
        filename_text = ("处理文件"
                        f"\n{indent}" 
                        "{}\n".format(
                                f'\n{indent}'
                                    .join(Filter
                                          (filedialog.askopenfilenames()))))
        
        manager.editor.insert(BEGIN, filename_text)
        
    return callback

def load_script(manager):
    def callback():
        """Load script codes from specific files.
        """
        filename = filedialog.askopenfilename()
        
        if not filename:
            return
        
        for encoding in CodecList:    
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    string = f.read()
                    manager.editor.delete(BEGIN, END)
                    manager.editor.insert(BEGIN, string)
                    break
            except UnicodeDecodeError:
                continue                    
        
    return callback


def remove_undef_col(old: pd.DataFrame):
    """Remove `Unnamed` fields. 
    """
    return old.loc[:,  [_ for _ in old.columns if not _.startswith('Unnamed')]]


def read_data(file_and_table):
    if len(file_and_table) is 1:
        file: str = file_and_table[0]
        return pd.read_csv(file) if file.lower().endswith('.csv') else pd.read_excel(file)
    return pd.read_excel(file_and_table[0], sheetname=file_and_table[1])

def write_date(df, filename):
    
    for encoding in CodecList:
        try:
            (lambda df: getattr(df, 
                            ['to_excel', 'to_csv'
                             ][int(filename.endswith('.csv'))]
                )(filename, encoding=encoding))(df)
        except UnicodeEncodeError:
            continue
        
    
    
class Manager:
    
    def __init__(self, log_path = os.path.abspath('./')):
        
        root = Tk() 
        root.title('grouping-helper')
        root.geometry() 
        root.iconbitmap('tmp.ico') 
        os.remove("./tmp.ico")

        # UI Layers
        editor = Text(root, height=20, width=50, font=CHINESEFONT)
        console = Text(root, height=20, width=30, font=CHINESEFONT)
        src_editor = Scrollbar(root, command=editor.yview)
        scr_console = Scrollbar(root, command=editor.yview)
        editor.configure(yscrollcommand=src_editor.set)
        console.configure(yscrollcommand=scr_console.set)
        
        select_file_btn = Button(root, 
                                 command=call_open_filenames(self), 
                                 text='选择数据')
        
        self.load_script = Button(root, 
                                  command=load_script(self), 
                                  text="导入工作计划")
        self.run_btn = Button(root,
                              command=self.run, 
                              text='生成结果')
        
        self.select_file_btn = select_file_btn
        self.console = console
        self.editor = editor
        self.root = root
        self.src_editor = src_editor
        self.scr_console = scr_console
        self.log_path = log_path
        self.display()
    
    def run(self):
        text = self.editor.get(BEGIN, END)
        parsed: dict = parse(self.editor.get(BEGIN, END))
        
        # logging
        for encoding in CodecList: 
            try:
                with open(f'{self.log_path}/日志.txt', 'a+', encoding=encoding) as f:
                    f.write('\n' + time.ctime() + '\n')
                    f.write(text)
                    break
            except UnicodeDecodeError:
                continue
            
        self.console.delete(BEGIN, END)
        if parsed['读入工作计划']:
            self.console.insert(END, "读入外部工作计划。\n")
            items = parsed['读入工作计划']
            for item in items:
                for encoding in CodecList:    
                    try:
                        with open(item, 'r', encoding=encoding) as f:
                            self.interpret(parse(f.read()))
                        break
                    except UnicodeDecodeError:
                        continue
        else:
            self.interpret(parsed)   
            
            
        
    def interpret(self, parsed):
        """In case of security it's not allowed to call scripts recursively.
        """
        
        err = []
        warn = []
        if not parsed['处理文件']:
            err.append('未输入待处理文件\n')
            self.console.insert(END, "Error:" + err[-1])
            return
        else:
            files = parsed['处理文件']
            
            if len(files) is not 1:
                warn.append('输入多个文件excel/csv文件时, 请保证各个文件的字段名一致\n')
                self.console.insert(END, "Warning:" + warn[-1])
                old = pd.concat([
                                remove_undef_col(read_data(file_and_table)) 
                                for file_and_table in 
                                map(lambda _: _.split('表名为'), files)])
            else:
                file = files[0]
                file_and_table = list(map(str.strip, file.split('表名为')))
                old = remove_undef_col(read_data(file_and_table))
            old.columns = old.columns.map(lambda _: _.replace('.', ''))
        
        old: pd.DataFrame
        new = pd.DataFrame(index=old.index)
        
        logics = list(Filter(parsed['选取']))
        selected = []
        
        for logic in [tuple(map(str.strip, logic.strip().split('='))) for logic in logics]:
            
            total = list(old.columns)
            total_arg_tps = ','.join(total)
            
            additional = True
            if len(logic) is 1:
                logic = logic*2 # (name, )*2
                additional = False

            new_name, define = logic
            fn_get_new_field = eval(f' lambda {total_arg_tps}: ({define})')
            values = old.loc[:, total].values
            
            selected.append(new_name)
            new[new_name] = list(Map(values, fn_get_new_field))
            
            if additional:
                old[new_name] = new[new_name]
        
            
        
        new.columns = selected
        output_rule = parsed['输出位置']
        
        if len(output_rule) is 0:
        
            err.append('没有给出输出位置。\n')
            self.console.insert(END, "Error:" + err[-1])
            return
        
        elif len(output_rule) > 1:
            
            warn.append('只会取第一个输出位置生成规则。\n')
            self.console.insert(END, "Warning:" + warn[-1])
       
        output_rule = output_rule[0]
        
        total_arg_tps = list(new.columns)
        total_arg_tps_ = ','.join(total_arg_tps)
        fn_group = eval(f'lambda {total_arg_tps_}: ({output_rule})')
        
        sort_fn = None
        
        if parsed['排序依据']:
            sort_expr = "({})".format(','.join([f for f in Filter(parsed['排序依据'])]))
            sort_fn = eval(f'lambda {total_arg_tps_}: ({sort_expr})')
        
        for outfile, arrs in GroupBy(new.values, fn_group).items():
            
            if sort_fn:
                arrs = sorted(arrs, key=lambda _:  sort_fn(*_))[::-1]
            
            write_date(
                    pd.DataFrame(
                        arrs, 
                        columns=total_arg_tps, 
                        index=range(1, len(arrs)+1)),
                    filename=outfile)
            
            self.console.insert(END, f'写入{outfile}\n')

        self.console.insert(END, "操作成功。\n")
        
        # logging errors and warnings.
        for encoding in CodecList: 
            try:
                with open(f'{self.log_path}/日志.txt', 'a+', encoding=encoding) as f:
                    if err:
                        f.write('Error(s):\t'  '\t\n'.join(err))
                    if warn:
                        f.write('Warnings(s):\t'  '\t\n'.join(warn))
                    break
            except UnicodeDecodeError:
                continue
     
            
    
    def display(self):
        """Fixed style
        """
        self.run_btn.grid(row=1, rowspan=1, column=0, columnspan=1, sticky=N+S+E+W, ipadx=50, pady=5)
        self.select_file_btn.grid(row=1, rowspan=1, column=2, columnspan=1, sticky=N+S+E+W, ipadx=50, pady=5)
        self.load_script.grid(row=1, rowspan=1, column=3, columnspan=1, sticky=N+S+E+W, ipadx=50, pady=5)
        self.editor.grid(row=3, rowspan=5, columnspan=10, column=0, sticky=N+S+E+W, pady=5)
        self.src_editor.grid(row=3, column=9, ipady=100)
        self.console.grid(row=3, rowspan=5, columnspan=5, column=10, sticky=N+S+E+W, pady=5)
        self.scr_console.grid(row=3, column=15, ipady=100)
    
        
if __name__ == '__main__':

    window = Manager()
    window.root.mainloop() 