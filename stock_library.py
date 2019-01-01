from database_setup import User, Base, Book, Genre
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///library.db',
                       connect_args={'check_same_thread': False})

# Bind the above engine to a session.
Session = sessionmaker(bind=engine)

# Create a Session object.
session = Session()


user1 = User(
    name='Lohith J',
    email='lohithj94@gmail.com',
    picture=''
)

session.add(user1)
session.commit()


# Books for Classic
genre1 = Genre(user=user1, name="Classic")
session.add(genre1)
session.commit()

item1 = Book(user=user1,
             name="A Christmas Carol",
             description="""A Christmas Carol. In Prose. Being a Ghost
                             Story ofChristmas,commonly known as A Christmas
                             Carol, is anovella by Charles Dickens,
                             first published in London by Chapman & Hall
                             in 1843 and illustrated by
                             John Leech. A Christmas Carol recounts the
                             story of Ebenezer Scrooge,
                             an elderly miser who is visited by the
                             ghost of his former business partner
                             Jacob Marley and the spirits of Christmas
                             Past, Present and Yet to Come.
                             After their visits, Scrooge is transformed
                             into a kinder, gentler man.""",
             author="Charles Dickens",
             publisher="Chapman & Hall",
             url="""https://books.google.co.in/books/content?id=rNhdhI_
                    iphYC&printsec=frontcover&img=1""",
             genre=genre1)
session.add(item1)
session.commit()

item2 = Book(user=user1,
             name="Macbeth",
             description="""A brave Scottish general named Macbeth
                             receives a prophecy from a trio of
                             witches that one day he will become King
                             of Scotland. Consumed by ambition and
                             spurred to action by his wife, Macbeth
                             murders King Duncan and takes the Scottish
                             throne for himself. He is then wracked
                             with guilt and paranoia. Forced to commit
                             more and more murders to protect himself
                             from enmity and suspicion, he soon becomes
                             a tyrannical ruler. The bloodbath and
                             consequent civil war swiftly take Macbeth
                             and Lady Macbeth into the realms of
                             madness and death.""",
             author="William Shakespeare",
             publisher="Folio",
             url="""https://books.google.co.in/books/content?id=/HysVAjLGOC0C&printsec=frontcover&img=1""",
             genre=genre1)
session.add(item2)
session.commit()


# Items for Comics/Graphic Novel
genre2 = Genre(user=user1, name="Comics/Graphic Novel")
session.add(genre2)
session.commit()

item1 = Book(user=user1,
             name="Explorers on the Moon",
             description="""Professor Calculus, Tintin, Snowy, Captain
                            Haddock, and Calculus' assistant Frank Wolff
                             are aboard an atomic rocket-powered spacecraft
                             leaving the Earth bound for the Moon. Soon
                             after takeoff they discover that the detectives
                             Thomson and Thompson have accidentally
                             stowed away onboard, putting a strain on the
                             oxygen supply. The detectives accidentally
                             turn off the nuclear motor, disrupting the
                             artificial gravity and sending everyone
                             floating until Tintin corrects the problem.
                             They then suffer a relapse of the Formula
                             14 drug , resulting in their hair growing
                             rapidly in multiple colours, until Calculus
                             subsequently  administers a cure. Haddock,
                             who has smuggled whisky aboard the rocket,
                             gets drunk and takes  an impromptu spacewalk,
                             during which he briefly becoming a satellite
                             of the asteroid Adonis
                             but Tintin is able to rescue him.""",
             author="Herge",
             publisher="Casterman",
             url="""https://upload.wikimedia.org/wikipedia/en/7/7c/The_Adventures_of_Tintin_-_17_-_Explorers_on_the_Moon.jpg""",
             genre=genre2)
session.add(item1)
session.commit()

item2 = Book(user=user1,
             name="Asterix the Gaul",
             description="""All Gaul is under Roman control, except for one
                             small village in Armorica, whose
                             inhabitants are made invincible by a magic
                             potion created periodically by the Druid Getafix.
                             To discover the secret of the Gauls' strength,
                              Centurion Crismus Bonus, commander of a Roman
                             garrison at the fortified camp of Compendium,
                              sends a spy disguised as a Gaul into the
                             village. The Roman's identity is revealed when
                              he loses his false moustache, shortly after he
                             discovers the existence of the magic potion;
                              whereupon he reports his discovery to the
                             Centurion.Crismus Bonus, hoping to overthrow
                             Julius Caesar, orders Getafix captured and
                             interrogated for the recipe; but to no avail.
                             Protagonist Asterix learns of Getafix's capture
                             from a cart-seller; infiltrates the Roman camp
                             in the latter's cart; and hears Crismus Bonus
                             revealing his intended rebellion to Marcus
                             Ginandtonicus, his second-in-command. Following
                             Asterix's suggestion, Getafix pretends to agree
                             to the Centurion's demand of the potion when
                             Asterix pretends to give in to torture, and
                             demands an unseasonal ingredient: strawberries.
                             While Crismus Bonus' soldiers try
                             to find strawberries, Asterix and Getafix relax
                             in relative luxury; and when the strawberries
                             arrive, consume them all, and console Crismus
                             Bonus that the potion may be made without them.
                             After all the ingredients are found, a potion is
                             prepared that causes the hair and beard of
                             the drinker to grow at an accelerated pace. The
                             Romans are tricked into drinking this potion
                             and before long, all of them have long hair and
                             beards. When Crismus Bonus pleads Getafix to
                             make an antidote, the druid makes a cauldron of
                             vegetable soup (knowing that the hair-growth
                             potion shall soon cease to take effect), and
                             also prepares a small quantity of the real magic
                             potion for Asterix. As Getafix and Asterix
                             escape, they are stopped by a huge army of
                             Roman reinforcements commanded by Julius Caesar.
                             Upon meeting Asterix and Getafix, Caesar hears
                             of Crismus Bonus' intentions against himself;
                             deports Crismus Bonus and his garrison to Outer
                             Mongolia; and frees Asterix and Getafix for
                             giving him the information, while reminding them
                             that they are still enemies. The two Gauls then
                             return to their village, where their neighbors
                             celebrate their recovery.""",
             author="Rene Goscinny",
             publisher="Dargaud",
             url="""https://upload.wikimedia.org/wikipedia/en/2/29/Asterixcover-asterix_the_gaul.jpg""",
             genre=genre2)
session.add(item2)
session.commit()


# Items for Fantasy
genre3 = Genre(user=user1, name="Fantasy")
session.add(genre3)
session.commit()

item1 = Book(user=user1,
             name="The Hobbit",
             description="""Gandalf tricks Bilbo into hosting a party
                            for Thorin and his band of dwarves, who sing
                             of reclaiming the Lonely Mountain and its vast
                             treasure from the dragon Smaug. When the music
                             ends, Gandalf unveils Thror's map showing a
                             secret door into the Mountain and proposes that
                             the dumbfounded Bilbo serve as the expedition's
                             "burglar". The dwarves ridicule the idea,
                             but Bilbo, indignant, joins despite himself.The
                             group travels into the wild, where Gandalf
                             saves the company from trolls and leads them to
                             Rivendell, where Elrond reveals more secrets
                             from the map. Passing over the Misty Mountains,
                             they are caught by goblins and driven deep
                             underground. Although Gandalf rescues them,
                             Bilbo gets separated from the others as they flee
                             the goblins. Lost in the goblin tunnels, he
                             stumbles across a mysterious ring and then
                             encountersGollum, who engages him in a
                             game of riddles.As a reward for solving
                             all riddles Gollum willshow him the path
                             out of the tunnels, but ifBilbo fails, his
                             life will be forfeit. With the help of the
                             ring, which confers invisibility, Bilbo
                             escapes and rejoins the dwarves, improving his
                             reputation with them. The goblins and Wargs give
                             chase, but the company are saved by eagles before
                             resting in the house of Beorn.""",
             author="J.R.R.Tolkien",
             publisher="George Allen & Unwin",
             url="""https://upload.wikimedia.org/wikipedia/en/a/a9/The_Hobbit_trilogy_dvd_cover.jpg""",
             genre=genre3)
session.add(item1)
session.commit()

item2 = Book(user=user1,
             name="Harry Potter and the Deathly Hallows",
             description="""Following Albus Dumbledore's death, Voldemort
                             consolidates his support and power, including
                             covert control of the Ministry of Magic, while
                             Harry is about to turn seventeen, losing the
                             protection of his home. The Order of the
                             Phoenix move Harry to a new location before
                             his birthday, but are attacked upon
                             departure. In the ensuing battle, "Mad-Eye"
                             Moody is killed and George Weasley wounded;
                             Voldemort himself arrives to kill Harry, but
                             Harry's wand fends him off of its own accord.
                             Harry, Ron and Hermione make preparations to
                             abandon Hogwarts and hunt down Voldemort's four
                             remaining Horcruxes, but have few clues to
                             work with as to their identities and locations.
                             One is a locket once owned by Hogwarts' co-founder
                             Salazar Slytherin which was stolen by the
                             mysterious "R.A.B.", one is possibly a cup
                             originally belonging to co-founder
                             Helga Hufflepuff, a third might be connected
                             to co-founder Rowena Ravenclaw, and the fourth
                             might be Nagini, Voldemort's snake familiar.
                             They also inherit strange bequests from among
                             Dumbledore's possessions: a Golden
                             Snitch for Harry, a Deluminator for Ron,
                             and a book of fairy tales for Hermione.""",
             author="J.K.Rowling",
             publisher="Bloomsbury",
             url="""https://upload.wikimedia.org/wikipedia/en/a/a9/Harry_Potter_and_the_Deathly_Hallows.jpg""",
             genre=genre3)
session.add(item2)
session.commit()


# Items for Biography
genre4 = Genre(user=user1, name="Biography")
session.add(genre4)
session.commit()

item1 = Book(user=user1,
             name="The Story of My Experiments with Truth",
             description="""The introduction is written by Gandhi
                                 himself mentioning how he has resumed
                                 writing his autobiographyat the
                                 insistence of Jeramdas, a fellow
                                 prisoner in Yerwada Central Jail with
                                 him. He mulls over the question a
                                  friend asked him about writing an
                                  autobiography, deeming it a Western
                                  practice, something "nobody does
                                  in the east". Gandhi himself agrees
                                  that his thoughts might change
                                  later in life but the purpose of his
                                  story is just to narrate his experiments
                                  with truth in life. He also says that
                                  through this book he wishes to narrate
                                  his spiritual and moral experiments
                                  rather than political.""",
             author="Mohandas Karamchand Gandhi",
             publisher="Young India",
             url="""https://upload.wikimedia.org/wikipedia/en/7/7e/The_Story_of_My_Experiments_with_Truth.jpg """,
             genre=genre4)


session.add(item1)
session.commit()


print ("Added First consinement of books")
