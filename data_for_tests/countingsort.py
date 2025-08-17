def counting_sort(A, k):
    
        C = [0] * k

        for i in range(len(A)):
            C[A[i] - 1] += 1;
        
        for i in range(1, len(C)):
            C[i] += C[i-1];
        
        B = [0] * len(A)

        for i in range(len(A) - 1, -1, -1):
            B[C[A[i] - 1] - 1] = A[i]
            C[A[i] - 1] -= 1

        return B;
    
