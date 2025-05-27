---
title: "What is a recurive function"
---
A recursive function looks like this:

    // Fibonacci sequence
    def fib(number)
        if number < 2
            number
        else
            fib(number - 1) + fib(number - 2)
        end
    end
