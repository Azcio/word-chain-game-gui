import random

# Track total points across multiple games
total_score = 0  

def load_chains(filename="data/word_chain.txt"):
    chains = []
    with open(filename, "r") as f:
        for line in f:
            words = [w.strip() for w in line.strip().split(",")]
            if words:
                chains.append(words)
    return chains

def play_game(difficulty="normal"):
    global total_score  # use global tracker

    chains = load_chains("data/word_chain.txt")
    random.shuffle(chains)

    session_score = 0

    for chain in chains:
        first_word = chain[0]
        hints = [first_word] + [word[0] for word in chain[1:]]
        print("\nChain hints:", " - ".join(hints))

        full_chain_cleared = True

        for i, actual in enumerate(chain[1:], start=2):

            if difficulty == "hard":
                # HARD MODE: 1 chance, no hints
                guess = input(f"Word {i} (starts with '{actual[0]}'): ").strip().lower()
                if guess == actual.lower():
                    print("✅ Correct! +100 points")
                    session_score += 100
                else:
                    print(f"❌ Wrong! The word was '{actual}'. Chain failed, restarting...")
                    full_chain_cleared = False
                    break

            else:
                # NORMAL MODE: 3 chances, hints allowed
                attempts = 0
                revealed = actual[0]
                word_score = 100
                got_word = False

                while attempts < 3:
                    print(f"Word {i} hint: {revealed}{'_' * (len(actual) - len(revealed))}")
                    guess = input(f"Guess word {i} (or type 'hint'): ").strip().lower()

                    if guess == "hint":
                        if len(revealed) < len(actual):
                            revealed += actual[len(revealed)]
                            word_score -= 10
                            print(f"🔍 Hint used! Current word score: {word_score}")
                        else:
                            print("⚠️ All letters revealed! No points possible now.")
                        continue

                    if guess == actual.lower():
                        if len(revealed) == len(actual):
                            print("✅ Correct, but no points (all letters revealed).")
                        else:
                            print(f"✅ Correct! +{word_score} points")
                            session_score += word_score
                        got_word = True
                        break
                    else:
                        attempts += 1
                        print(f"❌ Wrong! Attempts left: {3 - attempts}")

                if not got_word:
                    print(f"🚫 Out of chances! The word was '{actual}'")
                    full_chain_cleared = False

        # Chain complete bonus
        if difficulty == "normal" and full_chain_cleared:
            print("🎉 Chain completed with no mistakes! Bonus +50 points")
            session_score += 50

       # Calculate points earned this chain
        chain_points = session_score - total_score  

        # Update global total correctly
        total_score += chain_points  

    print(f"📊 Chain finished! This Chain: {chain_points} | Session Score: {session_score} | Total Score: {total_score}")


    print(f"\n🏆 Final Session Score: {session_score}")
    print(f"💯 Total Score (all games so far): {total_score}")

if __name__ == "__main__":
    while True:
        print("\nChoose difficulty: normal / hard (or type 'quit' to exit)")
        choice = input("Your choice: ").strip().lower()
        if choice == "quit":
            print(f"\n👋 Thanks for playing! Your final total score was {total_score}")
            break
        if choice not in ["normal", "hard"]:
            choice = "normal"
        play_game(choice)
