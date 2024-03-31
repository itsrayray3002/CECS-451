import sys

def update_belief_state(a, b, c, d, f, evidence_sequence):
    # Initialize belief state probabilities
    P_true = a
    P_false = 1 - a

    # Process each piece of evidence
    for evidence in evidence_sequence:
        # Update belief state based on evidence
        if evidence == 't':
            # Evidence is true
            P_true_evidence = P_true * d
            P_false_evidence = P_false * (1 - f)
        else:
            # Evidence is false
            P_true_evidence = P_true * (1 - d)
            P_false_evidence = P_false * f
        
        # Normalize the probabilities after evidence update
        norm = P_true_evidence + P_false_evidence
        P_true = P_true_evidence / norm
        P_false = P_false_evidence / norm

        # Update belief state based on state transitions
        P_true_next = P_true * b + P_false * (1 - c)
        P_false_next = P_true * (1 - b) + P_false * c

        # Normalize the probabilities after transition update
        P_true = P_true_next
        P_false = P_false_next

    return P_true, P_false

def process_input_file(file_path):
    # Open and process the input file
    with open(file_path, 'r') as file:
        for line in file:
            # Split the input line into components
            parts = line.strip().split(',')
            a, b, c, d, f = map(float, parts[:5])
            evidence_sequence = parts[5:]
            # Update belief state with the given evidence sequence
            P_true, P_false = update_belief_state(a, b, c, d, f, evidence_sequence)
            # Output the updated belief state, formatted correctly
            print(f"<{P_true:.4f},{P_false:.4f}>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hmm.py <input_file>", file=sys.stderr)
        sys.exit(1)
    process_input_file(sys.argv[1])
