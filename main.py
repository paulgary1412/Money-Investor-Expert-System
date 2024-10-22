from pyke import knowledge_engine

def ask_questions(engine):
    # Load questions from the KQB files and ask them dynamically
    questions = [
        'asking_money($amount, $has_money)',
        'asking_age($age, $is_age)'
    ]

    for question in questions:
        engine.reset()  # Reset the Pyke engine 
        print("Welcome to IBM Investor Center")

    
        engine.activate('questions.kqb')  # Activate the KQB file to ask the question
        engine.run(question)
        engine.assert_('fact.kfb', question[:-1])  # Assert the user's answer into the KFB
        # Ask whether the entered value is correct
        engine.activate('questions.kqb')  # Activate the KQB file again to ask the confirmation question
        engine.run('generic_yn("Is {} correct?", $confirm)'.format(question[:-1]))  # Ask confirmation question
        engine.assert_('fact.kfb', 'generic_yn("Is {} correct?", $confirm)'.format(question[:-1]))  # Assert confirmation answer into KFB

def main():
    # Load the Pyke knowledge engine
    engine = knowledge_engine.engine(__file__)

    # Ask questions and update the knowledge fact base (KFB)
    ask_questions(engine)

    # Run the Pyke knowledge engine with the updated KFB
    engine.activate('rules.krb')
    engine.run()
    
    # Print the rules fired
    print("Rules fired sequence:")
    print(", ".join(engine.list_queries()))

    # Check if goal is achieved
    if engine.goal_is_achieved():
        print("Conclusion :")
        print("Goal is achieved")
    else:
        print("Conclusion :")
        print("Goal is not achieved")

if __name__ == "__main__":
    main()
