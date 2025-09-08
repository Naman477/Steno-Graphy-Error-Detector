public class TestSplit {
    public static void main(String[] args) {
        String[] tests = {
            "The quick brown fox jumps over the lazy dog.",
            "This is a test. ",
            " One two three",
            "Apple   Orange   Banana"
        };
        for (String test : tests) {
            System.out.println("Input: '" + test + "'");
            String[] words = test.trim().split("\\s+");
            System.out.print("Output: [");
            for (int i = 0; i < words.length; i++) {
                System.out.print("'" + words[i] + "'");
                if (i < words.length - 1) {
                    System.out.print(", ");
                }
            }
            System.out.println("]");
        }
    }
}