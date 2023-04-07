from node import Node
from network import Network

ascii_art = '''
`7MMF'   `7MF'`7MM"""Mq.   .M"""bgd 
  `MA     ,V    MM   `MM. ,MI    "Y 
   VM:   ,V     MM   ,M9  `MMb.     
    MM.  M'     MMmmdM9     `YMMNq. 
    `MM A'      MM  YM.   .     `MM 
     :MM;       MM   `Mb. Mb     dM 
      VF      .JMML. .JMM.P"Ybmmd"  
      
        Vouch Reputation System
              EMPRESTA.ME
'''
print(ascii_art)

network = Network()

adam = network.add_node("Adam")
eve = network.add_node("Eve")
cain = network.add_node("Cain")
abel = network.add_node("Abel")
peter = network.add_node("Peter")

adam.vouch(eve, True, "I trust her")
adam.vouch(cain, True, "He's reliable")
adam.vouch(abel, True, "He's honest")

eve.vouch(adam, True, "He's trustworthy")
eve.vouch(cain, True, "I trust him")
eve.vouch(abel, True, "He's a good person")

cain.vouch(adam, True, "He's a good friend")
cain.vouch(eve, True, "She's dependable")
cain.vouch(abel, False, "I have doubts about his character")
cain.vouch(peter, True, "He's responsible")

abel.vouch(adam, True, "He's kind")
abel.vouch(eve, True, "She's genuine")

peter.vouch(cain, True, "He's hardworking") 
#peter.vouch("Abel", False)

network.calculate_reputation("Adam")
