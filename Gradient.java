import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;

public class Gradient {
    public static void main(String[] args) throws IOException {
        ArrayList<ArrayList<double[]>> gradients = new ArrayList<>();
        ArrayList<double[]> row = new ArrayList<>();
        double x, y, z, last = 0;

        try (BufferedReader reader = Files.newBufferedReader(Path.of("data/ncsutest.xyz"))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] tokens = line.split("\\s+");
                x = Double.parseDouble(tokens[0]);
                y = Double.parseDouble(tokens[1]);
                z = Double.parseDouble(tokens[2]);

                if (y != last) {
                    if (row.size() != 0) {
                        gradients.add(row);
                    }
                    row = new ArrayList<>();
                }
                
                row.add(new double[] {x, y, z});
                last = y;
            }
        }
    }
}